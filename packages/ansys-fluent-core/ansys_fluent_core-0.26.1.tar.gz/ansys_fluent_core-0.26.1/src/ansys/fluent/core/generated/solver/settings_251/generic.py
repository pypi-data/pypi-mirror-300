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

from .enabled_43 import enabled as enabled_cls
from .impact_angle_function import impact_angle_function as impact_angle_function_cls
from .diameter_function import diameter_function as diameter_function_cls
from .velocity_exponent_function import velocity_exponent_function as velocity_exponent_function_cls

class generic(Group):
    """
    Settings for the generic erosion model.
    """

    fluent_name = "generic"

    child_names = \
        ['enabled', 'impact_angle_function', 'diameter_function',
         'velocity_exponent_function']

    _child_classes = dict(
        enabled=enabled_cls,
        impact_angle_function=impact_angle_function_cls,
        diameter_function=diameter_function_cls,
        velocity_exponent_function=velocity_exponent_function_cls,
    )

    _child_aliases = dict(
        dpm_bc_erosion="impact_angle_function",
        dpm_bc_erosion_c="diameter_function",
        dpm_bc_erosion_generic="enabled",
        dpm_bc_erosion_n="velocity_exponent_function",
    )

