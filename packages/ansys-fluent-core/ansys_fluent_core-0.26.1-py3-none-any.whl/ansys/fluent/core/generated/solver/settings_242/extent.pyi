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

from .x_7 import x as x_cls
from .y_7 import y as y_cls
from .z_7 import z as z_cls

class extent(Group):
    fluent_name = ...
    child_names = ...
    x: x_cls = ...
    y: y_cls = ...
    z: z_cls = ...
