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

from .continuous_phase import continuous_phase as continuous_phase_cls
from .enable_rough_wall_treatment import enable_rough_wall_treatment as enable_rough_wall_treatment_cls
from .volume_displacement import volume_displacement as volume_displacement_cls

class interaction(Group):
    """
    'interaction' child.
    """

    fluent_name = "interaction"

    child_names = \
        ['continuous_phase', 'enable_rough_wall_treatment',
         'volume_displacement']

    _child_classes = dict(
        continuous_phase=continuous_phase_cls,
        enable_rough_wall_treatment=enable_rough_wall_treatment_cls,
        volume_displacement=volume_displacement_cls,
    )

    return_type = "<object object at 0x7ff9d2a0f250>"
