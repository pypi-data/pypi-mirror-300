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

from .prescribed import prescribed as prescribed_cls
from .value_16 import value as value_cls

class axis_1(Group):
    fluent_name = ...
    child_names = ...
    prescribed: prescribed_cls = ...
    value: value_cls = ...
