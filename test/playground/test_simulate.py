# FIXME: Include actual proper tests here!

from ippai.simulate import Tags
from ippai.simulate.simulation import simulate
from ippai.simulate.tissue_properties import get_muscle_settings
from ippai.simulate.structures import create_forearm_structures

import matplotlib.pylab as plt
import numpy as np

random_seed = 3287
np.random.seed(random_seed)
relative_shift = (np.random.random() - 0.5) * 2 * 12.5
background_oxy = (np.random.random() * 0.6) + 0.2
print(relative_shift)

settings = {
    Tags.WAVELENGTHS: [800], #np.arange(700, 951, 10),
    Tags.RANDOM_SEED: random_seed,
    Tags.VOLUME_NAME: "Forearm_"+str(random_seed).zfill(6),
    Tags.SIMULATION_PATH: "/home/janek/simulation_test/",
    Tags.RUN_OPTICAL_MODEL: True,
    Tags.OPTICAL_MODEL_NUMBER_PHOTONS: 1e8,
    Tags.OPTICAL_MODEL_BINARY_PATH: "/home/janek/simulation_test/mcx",#mcx_dkfz_probe",
    #Tags.OPTICAL_MODEL_PROBE_XML_FILE: "/home/janek/CAMI_PAT_SETUP_V2.xml",
    Tags.OPTICAL_MODEL: Tags.MODEL_MCX,
    Tags.RUN_ACOUSTIC_MODEL: False,
    'background_properties': get_muscle_settings(),
    Tags.SPACING_MM: 0.3,
    Tags.DIM_VOLUME_Z_MM: 30,
    Tags.DIM_VOLUME_X_MM: 40,
    Tags.DIM_VOLUME_Y_MM: 40,
    Tags.AIR_LAYER_HEIGHT_MM: 12,
    Tags.GELPAD_LAYER_HEIGHT_MM: 18,
    Tags.STRUCTURES: create_forearm_structures(relative_shift_mm=relative_shift, background_oxy=background_oxy)
}

[settings_path, optical_path, acoustic_path] = simulate(settings)
settings_data = np.load(settings_path[0])
optical_data = np.load(optical_path[0])

extent = [0, settings[Tags.DIM_VOLUME_X_MM], settings[Tags.DIM_VOLUME_Z_MM]+
          settings[Tags.AIR_LAYER_HEIGHT_MM] + settings[Tags.GELPAD_LAYER_HEIGHT_MM], 0]
air_height = int(settings[Tags.AIR_LAYER_HEIGHT_MM] / settings[Tags.SPACING_MM])
y_slice = int(int(settings[Tags.DIM_VOLUME_Y_MM] / settings[Tags.SPACING_MM]) / 2)
plt.figure(figsize=(7, 12))
plt.suptitle("Simulation without error")
plt.subplot(221)
plt.title("Segmentation along x axis")
plt.imshow(np.rot90(settings_data['seg'][:, y_slice, :], -1), extent=extent)
plt.colorbar()
plt.subplot(222)
plt.title("Initial pressure along x axis")
plt.imshow(np.log10(np.rot90(optical_data['initial_pressure'][:, y_slice, :], -1)), extent=extent)
plt.colorbar()
plt.subplot(223)
plt.title("Fluence along xy plane")
plt.imshow(np.log10(np.rot90(optical_data['fluence'][:, :, 1], -1)), extent=extent)
plt.colorbar()
plt.subplot(224)
plt.title("Fluence along yz plane")
plt.imshow(np.log10(np.rot90(optical_data['fluence'][:, y_slice - 1, :], -1)), extent=extent)
plt.colorbar()
plt.savefig(settings[Tags.SIMULATION_PATH] + "/simulation_without_error.png", dpi=300)
plt.close()
