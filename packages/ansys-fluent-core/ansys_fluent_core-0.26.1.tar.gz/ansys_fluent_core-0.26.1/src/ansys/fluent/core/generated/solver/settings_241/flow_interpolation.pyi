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

from .specific_heat_enabled import specific_heat_enabled as specific_heat_enabled_cls
from .density_enabled import density_enabled as density_enabled_cls
from .gradients_enabled import gradients_enabled as gradients_enabled_cls
from .viscosity_enabled import viscosity_enabled as viscosity_enabled_cls
from .temperature_enabled import temperature_enabled as temperature_enabled_cls
from .wall_zero_vel_enabled import wall_zero_vel_enabled as wall_zero_vel_enabled_cls

class flow_interpolation(Group):
    fluent_name = ...
    child_names = ...
    specific_heat_enabled: specific_heat_enabled_cls = ...
    density_enabled: density_enabled_cls = ...
    gradients_enabled: gradients_enabled_cls = ...
    viscosity_enabled: viscosity_enabled_cls = ...
    temperature_enabled: temperature_enabled_cls = ...
    wall_zero_vel_enabled: wall_zero_vel_enabled_cls = ...
    return_type = ...
