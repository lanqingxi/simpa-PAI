"""
SPDX-FileCopyrightText: 2021 Computer Assisted Medical Interventions Group, DKFZ
SPDX-FileCopyrightText: 2021 VISION Lab, Cancer Research UK Cambridge Institute (CRUK CI)
SPDX-License-Identifier: MIT
"""

from abc import abstractmethod
import numpy as np
from simpa.core.simulation_components import SimulationModule
from simpa.utils import Tags, Settings
from simpa.io_handling.io_hdf5 import save_hdf5
from simpa.utils.dict_path_manager import generate_dict_path


class AcousticForwardModelBaseAdapter(SimulationModule):
    """
    This method is the entry method for running an acoustic forward model.
    It is invoked in the *simpa.core.simulation.simulate* method, but can also be called
    individually for the purposes of performing acoustic forward modeling only or in a different context.

    The concrete will be chosen based on the::

        Tags.ACOUSTIC_MODEL

    tag in the settings dictionary.

    :param settings: The settings dictionary containing key-value pairs that determine the simulation.
        Here, it must contain the Tags.ACOUSTIC_MODEL tag and any tags that might be required by the specific
        acoustic model.
    :raises AssertionError: an assertion error is raised if the Tags.ACOUSTIC_MODEL tag is not given or
        points to an unknown acoustic forward model.
    """

    def __init__(self, global_settings: Settings):
        super(AcousticForwardModelBaseAdapter, self).__init__(global_settings=global_settings)
        self.component_settings = global_settings.get_acoustic_settings()

    @abstractmethod
    def forward_model(self) -> np.ndarray:
        """
        This method performs the acoustic forward modeling given the initial pressure
        distribution and the acoustic tissue properties contained in the settings file.
        A deriving class needs to implement this method according to its model.

        :return: time series pressure data
        """
        pass

    def run(self):
        """
        Call this method to invoke the simulation process.

        :param global_settings: the settings dictionary containing all simulation parameters.
        :return: a numpy array containing the time series pressure data per detection element
        """

        self.logger.info("Simulating the acoustic forward process...")

        time_series_data = self.forward_model()

        acoustic_output_path = generate_dict_path(Tags.TIME_SERIES_DATA, wavelength=self.global_settings[Tags.WAVELENGTH])

        save_hdf5(time_series_data, self.global_settings[Tags.SIMPA_OUTPUT_PATH], acoustic_output_path)

        self.logger.info("Simulating the acoustic forward process...[Done]")
