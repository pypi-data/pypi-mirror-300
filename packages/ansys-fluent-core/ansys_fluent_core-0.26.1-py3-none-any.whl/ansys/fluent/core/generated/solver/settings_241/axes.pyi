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

from .x_1 import x as x_cls
from .y_1 import y as y_cls
from .background_color import background_color as background_color_cls

class axes(Group):
    fluent_name = ...
    child_names = ...
    x: x_cls = ...
    y: y_cls = ...
    background_color: background_color_cls = ...
    return_type = ...
