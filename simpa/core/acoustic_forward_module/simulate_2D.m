 %% The MIT License (MIT)
%%
%% Copyright (c) 2021 Computer Assisted Medical Interventions Group, DKFZ
%%
%% Permission is hereby granted, free of charge, to any person obtaining a copy
%% of this software and associated documentation files (the "Software"), to deal
%% in the Software without restriction, including without limitation the rights
%% to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
%% copies of the Software, and to permit persons to whom the Software is
%% furnished to do so, subject to the following conditions:
%%
%% The above copyright notice and this permission notice shall be included in all
%% copies or substantial portions of the Software.
%%
%% THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
%% IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
%% FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
%% AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
%% LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
%% OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
%% SOFTWARE.

function [] = simulate_2D(optical_path)

%% In case of an error, make sure the matlab scripts exits anyway
clean_up = onCleanup(@exit);

%% Read settings file

data = load(optical_path);
settings = data.settings;

%% Read initial pressure

source.p0 = data.initial_pressure;

%% Define kWaveGrid

% add 2 pixel "gel" to reduce Fourier artifact
GEL_LAYER_HEIGHT = 2;

source.p0 = padarray(source.p0, [GEL_LAYER_HEIGHT 0], 0, 'pre');
[Nx, Ny] = size(source.p0);
if isfield(settings, 'sample') == true
    if settings.sample == true
        dx = double(settings.voxel_spacing_mm)/(double(settings.upscale_factor) * 1000);
    else
        dx = double(settings.voxel_spacing_mm)/1000;    % convert from mm to m
    end
else
    dx = double(settings.voxel_spacing_mm)/1000;    % convert from mm to m
end
kgrid = kWaveGrid(Nx, dx, Ny, dx);

%% Define medium

% if a field of the struct "data" is given which describes the sound speed, the array is loaded and is used as medium.sound_speed
if isfield(data, 'sos') == true
    medium.sound_speed = data.sos;
    % add 2 pixel "gel" to reduce Fourier artifact
    medium.sound_speed = padarray(medium.sound_speed, [GEL_LAYER_HEIGHT 0], 'replicate', 'pre');
else
    medium.sound_speed = 1540;
end

% if a field of the struct "data" is given which describes the attenuation, the array is loaded and is used as medium.alpha_coeff
if isfield(data, 'alpha_coeff') == true
 medium.alpha_coeff = data.alpha_coeff;
 % add 2 pixel "gel" to reduce Fourier artifact
 medium.alpha_coeff = padarray(medium.alpha_coeff, [GEL_LAYER_HEIGHT 0], 'replicate', 'pre');
else
 medium.alpha_coeff = 0.01;
end

medium.alpha_power = double(settings.medium_alpha_power); % b for a * MHz ^ b

% if a field of the struct "data" is given which describes the density, the array is loaded and is used as medium.density
if isfield(data, 'density') == true
    medium.density = data.density;
    % add 2 pixel "gel" to reduce Fourier artifact
    medium.density = padarray(medium.density, [GEL_LAYER_HEIGHT 0], 'replicate', 'pre');
else
    medium.density = 1000*ones(Nx, Ny);
end

kgrid.t_array = makeTime(kgrid, medium.sound_speed, 0.3);	% time array with
% CFL number of 0.3 (advised by manual)
% Using makeTime, dt = CFL*dx/medium.sound_speed and the total
% time is set to the time it would take for an acoustic wave to travel
% across the longest grid diagonal.

%% Define sensor

% create empty array
karray = kWaveArray;

elem_pos = data.sensor_element_positions/1000;

% In case some detectors are defined at zeros or with negative values out
% of bounds, correct all of them with minimum need correction 0.0001.

min_x_pos = find(elem_pos(1, :) <= 0);
min_y_pos = find(elem_pos(2, :) <= 0);
x_correction = 0;
y_correction = 0;
if size(min_x_pos) > 0
   x_correction = 0.0001;
end

if size(min_y_pos) > 0
   y_correction = 0.0001;
end

elem_pos(1, :) = elem_pos(1, :) - 0.5*kgrid.x_size + x_correction;
elem_pos(2, :) = elem_pos(2, :) - 0.5*kgrid.y_size + y_correction;
num_elements = size(elem_pos, 2);

element_width = double(settings.detector_element_width_mm)/1000;
angles = data.directivity_angle;

if isfield(settings, 'sensor_radius_mm') == true
    radius_of_curv = double(settings.sensor_radius_mm)/1000;
end

% For addArcElement orient all elements towards the focus
% For the iThera MSOT Acuity Echo, it is [0.008, 0]

%focus_pos = [0.008, 0];

% add elements to the array

%for ind = 1:num_elements
%    karray.addArcElement(elem_pos(:, ind), radius_of_curv, element_width, focus_pos);
%end
for ind = 1:num_elements
  x = elem_pos(1, ind);
  y = elem_pos(2, ind);
  alpha = angles(1, ind);
%  x2=x+0.5*(element_width*sin(alpha));
%  y2=y+0.5*(element_width*cos(alpha));
  x = x - 0.5*(element_width*sin(alpha));
  y = y - 0.5*(element_width*cos(alpha));
  karray.addRectElement([x, y], element_width, 0.00001, [angles(1, ind)]);
%  karray.addLineElement([x, y], [x2, y2]);
end

% if a field of the struct "data" is given which describes the sensor directivity angles, the array is loaded and is used as sensor.directivity_angle
%if isfield(data, 'directivity_angle') == true
%    sensor.directivity_angle = data.directivity_angle;
%    % add 2 pixel "gel" to reduce Fourier artifact
%    sensor.directivity_angle = padarray(sensor.directivity_angle, [GEL_LAYER_HEIGHT 0], 0, 'pre');
%end
%
%if isfield(data, 'directivity_size')
%    sensor.directivity_size = settings.sensor_directivity_size;
%end

%% Computation settings

if settings.gpu == true
    datacast = 'gpuArray-single';
else
    datacast = 'single';
end

input_args = {'DataCast', datacast, 'PMLInside', settings.pml_inside, ...
              'PMLAlpha', settings.pml_alpha, 'PMLSize', 'auto', ...
              'PlotPML', settings.plot_pml, 'RecordMovie', settings.record_movie, ...
              'MovieName', settings.movie_name, 'PlotScale', [-1, 1], 'LogScale', settings.acoustic_log_scale};

% assign binary mask from karray to the sensor mask
sensor.mask = karray.getArrayBinaryMask(kgrid);
center_freq = double(settings.sensor_center_frequency); % [Hz]
bandwidth = double(settings.sensor_bandwidth); % [%]
sensor.frequency_response = [center_freq, bandwidth];

if settings.gpu == true
    time_series_data = kspaceFirstOrder2DG(kgrid, medium, source, sensor, input_args{:});
    time_series_data = gather(time_series_data);
else
    time_series_data = kspaceFirstOrder2D(kgrid, medium, source, sensor, input_args{:});
end

% combine data to give one trace per physical array element
time_series_data = karray.combineSensorData(kgrid, time_series_data);

%% Write data to mat array
save(optical_path, 'time_series_data')%, '-v7.3')
time_step = kgrid.dt;
number_time_steps = kgrid.Nt;
save(strcat(optical_path, 'dt.mat'), 'time_step', 'number_time_steps');

end