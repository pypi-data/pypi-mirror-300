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

from .pressure_jump_specification import pressure_jump_specification as pressure_jump_specification_cls
from .swirl_velocity_specification import swirl_velocity_specification as swirl_velocity_specification_cls
from .discrete_phase_2 import discrete_phase as discrete_phase_cls
from .geometry_2 import geometry as geometry_cls
from .phase_35 import phase as phase_cls

class settings(Group):
    """
    Select domain name to define settings on.
    """

    fluent_name = "settings"

    child_names = \
        ['pressure_jump_specification', 'swirl_velocity_specification',
         'discrete_phase', 'geometry', 'phase']

    _child_classes = dict(
        pressure_jump_specification=pressure_jump_specification_cls,
        swirl_velocity_specification=swirl_velocity_specification_cls,
        discrete_phase=discrete_phase_cls,
        geometry=geometry_cls,
        phase=phase_cls,
    )

    _child_aliases = dict(
        dpm="discrete_phase",
    )

