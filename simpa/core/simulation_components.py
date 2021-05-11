"""
SPDX-FileCopyrightText: 2021 Computer Assisted Medical Interventions Group, DKFZ
SPDX-FileCopyrightText: 2021 VISION Lab, Cancer Research UK Cambridge Institute (CRUK CI)
SPDX-License-Identifier: MIT
"""

from abc import abstractmethod, ABC
from simpa.log import Logger
from simpa.utils import Settings


class SimulationModule:
    """
    Defines a simulation module that is callable via the SIMPA core.simulation.simulate method.
    """

    def __init__(self, global_settings: Settings):
        """
        Initialises the SimulationModule given the global settings dictionary.
         :param global_settings: The SIMPA settings dictionary
        """
        self.logger = Logger()
        self.global_settings = global_settings

    @abstractmethod
    def run(self):
        """
        Executes the respective simulation module

        :param global_settings: The global SIMPA settings dictionary
        """
        pass


class ProcessingComponent(SimulationModule, ABC):
    """
    Defines a simulation component, which can be used to pre- or post-process simulation data.
    """

    def __init__(self, global_settings, component_settings_key: str):
        """
        Initialises the ProcessingComponent.

        :param component_settings_key: The key where the component settings are stored in
        """
        super(ProcessingComponent, self).__init__(global_settings=global_settings)
        self.component_settings = global_settings[component_settings_key]