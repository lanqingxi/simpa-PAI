# The MIT License (MIT)
#
# Copyright (c) 2018 Computer Assisted Medical Interventions Group, DKFZ
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated simpa_documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from simpa.utils import Tags
from simpa.core.image_reconstruction import ReconstructionAdapterBase
from simpa.utils.dict_path_manager import generate_dict_path
from simpa.io_handling.io_hdf5 import load_hdf5
from simpa.core.device_digital_twins import DEVICE_MAP
import numpy as np
import torch
import torch.fft
from scipy.signal import hilbert
from scipy.signal.windows import tukey

from simpa.utils.settings_generator import Settings

class InvalidBandpassFilterCutoffValueError(Exception):
    """Raised when the given cutoff values are either too small or too large"""
    pass


class PyTorchDASAdapter(ReconstructionAdapterBase):
    def reconstruction_algorithm(self, time_series_sensor_data, settings):
        """
        Applies the Delay and Sum beamforming algorithm [1] to the time series sensor data (2D numpy array where the first dimension corresponds to the sensor elements
        and the second to the recorded time steps) with the given beamforming settings (dictionary).
        A reconstructed image (2D numpy array) is returned.
        This implementation uses PyTorch Tensors to perform computations and is able to run on GPUs.

        [1] T. Kirchner et al. 2018, "Signed Real-Time Delay Multiply and Sum Beamformingfor Multispectral Photoacoustic Imaging", https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&ved=2ahUKEwi3hZjA48jtAhUM6OAKHWK-BuAQFjAAegQIBxAC&url=https%3A%2F%2Fwww.mdpi.com%2F2313-433X%2F4%2F10%2F121%2Fpdf&usg=AOvVaw3CCZEt7L_xoUbWvlW1Ljx5
        """

        # check for B-mode methods and envelope detection straight away
        if Tags.RECONSTRUCTION_BMODE_METHOD in settings:
            if settings[Tags.RECONSTRUCTION_BMODE_METHOD] == Tags.RECONSTRUCTION_BMODE_METHOD_HILBERT_TRANSFORM:
                # perform envelope detection using hilbert transform
                hilbert_transformed = hilbert(time_series_sensor_data, axis=1)
                time_series_sensor_data = np.abs(hilbert_transformed)

            if settings[Tags.RECONSTRUCTION_BMODE_METHOD] == Tags.RECONSTRUCTION_BMODE_METHOD_ABS:
                # perform envelope detection using absolute value
                time_series_sensor_data = np.abs(time_series_sensor_data)
        else:
            print("You have not specified a B-mode method")

        ### INPUT CHECKING AND VALIDATION ###
        # check settings dictionary for elements and read them in

        # speed of sound
        if Tags.PROPERTY_SPEED_OF_SOUND in settings and settings[Tags.PROPERTY_SPEED_OF_SOUND]:
            speed_of_sound_in_m_per_s = settings[Tags.PROPERTY_SPEED_OF_SOUND]
        elif Tags.WAVELENGTH in settings and settings[Tags.WAVELENGTH]:
            acoustic_data_path = generate_dict_path(settings, Tags.PROPERTY_SPEED_OF_SOUND,
                                                    wavelength=settings[Tags.WAVELENGTH], upsampled_data=True)
            sound_speed_m = load_hdf5(settings[Tags.SIMPA_OUTPUT_PATH], acoustic_data_path)[
                Tags.PROPERTY_SPEED_OF_SOUND]
            speed_of_sound_in_m_per_s = np.mean(sound_speed_m)
        else:
            raise AttributeError("Please specify a value for PROPERTY_SPEED_OF_SOUND or WAVELENGTH to obtain the average speed of sound")

        # time spacing: use sampling rate is specified, otherwise kWave specific dt from simulation
        if Tags.SENSOR_SAMPLING_RATE_MHZ in settings and settings[Tags.SENSOR_SAMPLING_RATE_MHZ]:
            time_spacing_in_ms = 1.0 / (settings[Tags.SENSOR_SAMPLING_RATE_MHZ] * 1000)
        elif Tags.K_WAVE_SPECIFIC_DT in settings and settings[Tags.K_WAVE_SPECIFIC_DT]:
            time_spacing_in_ms = settings[Tags.K_WAVE_SPECIFIC_DT] * 1000
        else:
            raise AttributeError("Please specify a value for SENSOR_SAMPLING_RATE_MHZ or K_WAVE_SPECIFIC_DT")

        # spacing
        if Tags.SPACING_MM in settings and settings[Tags.SPACING_MM]:
            sensor_spacing_in_mm = settings[Tags.SPACING_MM]
        else:
            raise AttributeError("Please specify a value for SPACING_MM")

        # get device specific sensor positions
        device = DEVICE_MAP[settings[Tags.DIGITAL_DEVICE]]
        device.check_settings_prerequisites(settings)
        device.adjust_simulation_volume_and_settings(settings)

        sensor_positions = device.get_detector_element_positions_accounting_for_device_position_mm(settings)
        sensor_positions = np.round(sensor_positions / sensor_spacing_in_mm).astype(int)
        sensor_positions = np.array(sensor_positions[:, [0, 2]])  # only use x and y positions and ignore z

        # time series sensor data must be numpy array
        if isinstance(sensor_positions, np.ndarray):
            sensor_positions = torch.from_numpy(sensor_positions)
        if isinstance(time_series_sensor_data, np.ndarray):
            time_series_sensor_data = torch.from_numpy(time_series_sensor_data)
        assert isinstance(time_series_sensor_data,
                          torch.Tensor), 'The time series sensor data must have been converted to a tensor'

        # move tensors to GPU if available, otherwise use CPU
        if Tags.GPU not in settings:
            if torch.cuda.is_available():
                dev = "cuda"
            else:
                dev = "cpu"
        else:
            dev = "cuda" if settings[Tags.GPU] else "cpu"

        device = torch.device(dev)
        sensor_positions = sensor_positions.to(device)
        time_series_sensor_data = time_series_sensor_data.to(device)

        # array must be of correct dimension
        assert time_series_sensor_data.ndim == 2, 'Samples must have exactly 2 dimensions. ' \
                                                  'Apply beamforming per wavelength if you have a 3D array. '

        ### ALGORITHM ITSELF ###

        # apply by default bandpass filter using tukey window with alpha=0.5 on time series data in frequency domain
        if Tags.RECONSTRUCTION_PERFORM_BANDPASS_FILTERING not in settings or settings[
            Tags.RECONSTRUCTION_PERFORM_BANDPASS_FILTERING] is not False:

            # construct bandpass filter given the cutoff values and time spacing
            frequencies = np.fft.fftfreq(time_series_sensor_data.shape[1], d=time_spacing_in_ms/1000)
            cutoff_lowpass = settings[Tags.BANDPASS_CUTOFF_LOWPASS] if Tags.BANDPASS_CUTOFF_LOWPASS in settings else int(8e6)
            cutoff_highpass = settings[Tags.BANDPASS_CUTOFF_HIGHPASS] if Tags.BANDPASS_CUTOFF_HIGHPASS in settings else int(0.1e6)
            if cutoff_highpass > cutoff_lowpass:
                raise InvalidBandpassFilterCutoffValueError("The highpass cutoff value must be lower than the lowpass cutoff value.")
            try:
                small_index = np.where(frequencies == cutoff_highpass)[0][0]
            except IndexError:
                raise InvalidBandpassFilterCutoffValueError(f"The highpass cutoff value is invalid for the given time spacing. "
                      f"Please set it to {np.min(frequencies)} at least.")
            try:
                large_index = np.where(frequencies == cutoff_lowpass)[0][0]
            except IndexError:
                raise InvalidBandpassFilterCutoffValueError(f"The lowpass cutoff value is invalid for the given time spacing."
                     f" Please set it to {np.max(frequencies)} at max.")

            tukey_alpha = settings[Tags.TUKEY_WINDOW_ALPHA] if Tags.TUKEY_WINDOW_ALPHA in settings else 0.5
            win = torch.tensor(tukey(large_index - small_index, alpha = tukey_alpha), device=device)
            window = torch.zeros(frequencies.shape, device=device)
            window[small_index:large_index] = win

            # transform data into Fourier space, multiply filter and transform back
            TIME_SERIES_SENSOR_DATA = torch.fft.fft(time_series_sensor_data)
            FILTERED = TIME_SERIES_SENSOR_DATA * window.expand_as(TIME_SERIES_SENSOR_DATA)
            time_series_sensor_data = torch.abs(torch.fft.ifft(FILTERED))

        ## compute size of beamformed image ##
        xdim = (max(sensor_positions[:, 0]) - min(sensor_positions[:, 0]))
        xdim = int(xdim) + 1  # correction due to subtraction of indices starting at 0
        ydim = float(
            time_series_sensor_data.shape[1] * time_spacing_in_ms * speed_of_sound_in_m_per_s) / sensor_spacing_in_mm
        ydim = int(round(ydim))
        n_sensor_elements = time_series_sensor_data.shape[0]

        print(f'Number of pixels in X dimension: {xdim}, Y dimension: {ydim}, sensor elements: {n_sensor_elements}')

        # construct output image
        output = torch.zeros((xdim, ydim), dtype=torch.float32, device=device)

        xx, yy, jj = torch.meshgrid(torch.arange(xdim, device=device),
                                    torch.arange(ydim, device=device),
                                    torch.arange(n_sensor_elements, device=device))

        delays = torch.sqrt(((yy - sensor_positions[:, 1][jj]) * sensor_spacing_in_mm) ** 2 +
                            ((xx - torch.abs(sensor_positions[:, 0][jj])) * sensor_spacing_in_mm) ** 2) \
                 / (speed_of_sound_in_m_per_s * time_spacing_in_ms)

        delays = torch.round(delays).long()

        # perform index validation
        invalid_indices = torch.where(torch.logical_or(delays < 0, delays >= float(time_series_sensor_data.shape[1])))
        delays[invalid_indices] = 0

        # check for apodization method
        if Tags.RECONSTRUCTION_APODIZATION_METHOD in settings:
            # hann window
            if settings[Tags.RECONSTRUCTION_APODIZATION_METHOD] == Tags.RECONSTRUCTION_APODIZATION_HANN:
                hann = torch.hann_window(n_sensor_elements, device=device)
                apodization = hann.expand((xdim, ydim, n_sensor_elements))
            # hamming window
            elif settings[Tags.RECONSTRUCTION_APODIZATION_METHOD] == Tags.RECONSTRUCTION_APODIZATION_HAMMING:
                hamming = torch.hamming_window(n_sensor_elements, device=device)
                apodization = hamming.expand((xdim, ydim, n_sensor_elements))
            # box window apodization as default
            else:
                apodization = torch.ones((xdim, ydim, n_sensor_elements), device=device)
        else:
            # box window apodization as default
            apodization = torch.ones((xdim, ydim, n_sensor_elements), device=device)

        values = time_series_sensor_data[jj, delays] * apodization

        # set values of invalid indices to 0 so that they don't influence the result
        values[invalid_indices] = 0
        sum = torch.sum(values, dim=2)
        counter = torch.count_nonzero(values, dim=2)
        torch.divide(sum, counter, out=output)

        reconstructed = np.flipud(output.cpu().numpy())

        return reconstructed


def reconstruct_DAS_PyTorch(time_series_sensor_data, settings=None):
    """
    Convenience function for reconstructing time series data using Delay and Sum algorithm implemented in PyTorch
    :param time_series_sensor_data: 2D numpy array of sensor data of shape (sensor elements, time steps)
    :return: reconstructed image as 2D numpy array
    """
    adapter = PyTorchDASAdapter()
    return adapter.reconstruction_algorithm(time_series_sensor_data, settings)


def reconstruct_DAS_PyTorch(time_series_sensor_data, settings = None, sound_of_speed=1500, time_spacing=2.5e-8, sensor_spacing=0.1):
    """
    Convenience function for reconstructing time series data using Delay and Sum algorithm implemented in PyTorch
    :param time_series_sensor_data: 2D numpy array of sensor data of shape (sensor elements, time steps)
    :param settings: settings dictionary (by default there is none and the other parameters are used instead)
    :param sound_of_speed: speed of sound in medium in meters per second (default: 1500 m/s)
    :param time_spacing: time between sampling points in seconds (default: 2.5e-8 s which is equal to 40 MHz)
    :param sensor_spacing: space between sensor elements in millimeters (default: 0.1 mm)
    :return: reconstructed image as 2D numpy array
    """

    # create settings if they don't exist yet
    if settings is None:
        settings = Settings()

        # parse reconstruction settings
        #settings[Tags.PROPERTY_SPEED_OF_SOUND] = sound_of_speed
        settings[Tags.SENSOR_SAMPLING_RATE_MHZ] = (1.0 / time_spacing) / 1000000
        settings[Tags.SPACING_MM] = sensor_spacing

    adapter = PyTorchDASAdapter()
    return adapter.reconstruction_algorithm(time_series_sensor_data, settings)
