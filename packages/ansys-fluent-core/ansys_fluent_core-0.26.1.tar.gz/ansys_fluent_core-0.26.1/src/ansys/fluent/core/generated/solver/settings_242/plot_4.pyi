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

from .x_axis_function import x_axis_function as x_axis_function_cls
from .enabled_45 import enabled as enabled_cls

class plot(Group):
    fluent_name = ...
    child_names = ...
    x_axis_function: x_axis_function_cls = ...
    enabled: enabled_cls = ...
