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

from .first_axis import first_axis as first_axis_cls
from .auto_second_axis import auto_second_axis as auto_second_axis_cls
from .second_axis import second_axis as second_axis_cls

class orientation(Group):
    fluent_name = ...
    child_names = ...
    first_axis: first_axis_cls = ...
    auto_second_axis: auto_second_axis_cls = ...
    second_axis: second_axis_cls = ...
