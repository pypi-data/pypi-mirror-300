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

from .x_displacement_type import x_displacement_type as x_displacement_type_cls
from .x_displacement_value import x_displacement_value as x_displacement_value_cls
from .y_displacement_type import y_displacement_type as y_displacement_type_cls
from .y_displacement_value import y_displacement_value as y_displacement_value_cls
from .z_displacement_type import z_displacement_type as z_displacement_type_cls
from .z_displacement_value import z_displacement_value as z_displacement_value_cls

class structure(Group):
    fluent_name = ...
    child_names = ...
    x_displacement_type: x_displacement_type_cls = ...
    x_displacement_value: x_displacement_value_cls = ...
    y_displacement_type: y_displacement_type_cls = ...
    y_displacement_value: y_displacement_value_cls = ...
    z_displacement_type: z_displacement_type_cls = ...
    z_displacement_value: z_displacement_value_cls = ...
    return_type = ...
