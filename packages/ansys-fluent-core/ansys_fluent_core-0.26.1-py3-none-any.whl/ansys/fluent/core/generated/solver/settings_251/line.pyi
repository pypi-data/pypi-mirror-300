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

from .pattern import pattern as pattern_cls
from .weight_1 import weight as weight_cls
from .color_1 import color as color_cls

class line(Group):
    fluent_name = ...
    child_names = ...
    pattern: pattern_cls = ...
    weight: weight_cls = ...
    color: color_cls = ...
