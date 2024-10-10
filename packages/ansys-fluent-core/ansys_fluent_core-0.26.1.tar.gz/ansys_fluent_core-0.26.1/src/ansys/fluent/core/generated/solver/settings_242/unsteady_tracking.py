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

from .enabled_3 import enabled as enabled_cls
from .option_5 import option as option_cls
from .create_particles_at import create_particles_at as create_particles_at_cls
from .dpm_time_step_size import dpm_time_step_size as dpm_time_step_size_cls
from .number_of_time_steps import number_of_time_steps as number_of_time_steps_cls
from .clear_all_particles import clear_all_particles as clear_all_particles_cls

class unsteady_tracking(Group):
    """
    Group containing unsteady particle tracking related settings.
    """

    fluent_name = "unsteady-tracking"

    child_names = \
        ['enabled', 'option', 'create_particles_at', 'dpm_time_step_size',
         'number_of_time_steps']

    command_names = \
        ['clear_all_particles']

    _child_classes = dict(
        enabled=enabled_cls,
        option=option_cls,
        create_particles_at=create_particles_at_cls,
        dpm_time_step_size=dpm_time_step_size_cls,
        number_of_time_steps=number_of_time_steps_cls,
        clear_all_particles=clear_all_particles_cls,
    )

    _child_aliases = dict(
        create_particles_every_dpm_step="create_particles_at",
    )

