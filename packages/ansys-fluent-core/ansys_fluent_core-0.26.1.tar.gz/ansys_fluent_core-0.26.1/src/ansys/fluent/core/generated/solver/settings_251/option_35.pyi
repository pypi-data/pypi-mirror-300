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

from .option_1 import option as option_cls
from .yplus_1 import yplus as yplus_cls
from .ystar import ystar as ystar_cls

class option(Group):
    fluent_name = ...
    child_names = ...
    option: option_cls = ...
    yplus: yplus_cls = ...
    ystar: ystar_cls = ...
