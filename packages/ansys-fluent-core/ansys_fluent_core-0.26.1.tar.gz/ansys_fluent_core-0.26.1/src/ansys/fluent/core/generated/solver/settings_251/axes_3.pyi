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

from .border import border as border_cls
from .bottom import bottom as bottom_cls
from .clear_1 import clear as clear_cls
from .left import left as left_cls
from .right_1 import right as right_cls
from .top import top as top_cls
from .visible_2 import visible as visible_cls

class axes(Group):
    fluent_name = ...
    child_names = ...
    border: border_cls = ...
    bottom: bottom_cls = ...
    clear: clear_cls = ...
    left: left_cls = ...
    right: right_cls = ...
    top: top_cls = ...
    visible: visible_cls = ...
