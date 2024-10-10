#
# This is an auto-generated file.  DO NOT EDIT!
#


from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import (
    _ChildNamedObjectAccessorMixin,
    CreatableNamedObjectMixin,
    _NonCreatableNamedObjectMixin,
    AllowedValuesMixin,
    _InputFile,
    _OutputFile,
    _InOutFile,
)

from typing import Union, List, Tuple

from .option_3 import option as option_cls
from .particle_creation_every_particle_step_enabled import particle_creation_every_particle_step_enabled as particle_creation_every_particle_step_enabled_cls
from .dpm_time_step import dpm_time_step as dpm_time_step_cls
from .n_time_steps import n_time_steps as n_time_steps_cls
from .clear_particles_from_domain import clear_particles_from_domain as clear_particles_from_domain_cls

class unsteady_tracking(Group):
    fluent_name = ...
    child_names = ...
    option: option_cls = ...
    particle_creation_every_particle_step_enabled: particle_creation_every_particle_step_enabled_cls = ...
    dpm_time_step: dpm_time_step_cls = ...
    n_time_steps: n_time_steps_cls = ...
    command_names = ...

    def clear_particles_from_domain(self, ):
        """
        Clear all particles currently in the domain.
        """

    return_type = ...
