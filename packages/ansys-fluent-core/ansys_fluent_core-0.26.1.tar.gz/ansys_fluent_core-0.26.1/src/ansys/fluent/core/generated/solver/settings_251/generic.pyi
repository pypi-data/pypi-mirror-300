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

from .enabled_43 import enabled as enabled_cls
from .impact_angle_function import impact_angle_function as impact_angle_function_cls
from .diameter_function import diameter_function as diameter_function_cls
from .velocity_exponent_function import velocity_exponent_function as velocity_exponent_function_cls

class generic(Group):
    fluent_name = ...
    child_names = ...
    enabled: enabled_cls = ...
    impact_angle_function: impact_angle_function_cls = ...
    diameter_function: diameter_function_cls = ...
    velocity_exponent_function: velocity_exponent_function_cls = ...
