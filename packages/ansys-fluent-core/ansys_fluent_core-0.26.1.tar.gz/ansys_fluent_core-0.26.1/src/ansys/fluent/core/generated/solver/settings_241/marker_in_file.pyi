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

from .symbol import symbol as symbol_cls
from .size import size as size_cls
from .color_1 import color as color_cls

class marker_in_file(Group):
    fluent_name = ...
    child_names = ...
    symbol: symbol_cls = ...
    size: size_cls = ...
    color: color_cls = ...
    return_type = ...
