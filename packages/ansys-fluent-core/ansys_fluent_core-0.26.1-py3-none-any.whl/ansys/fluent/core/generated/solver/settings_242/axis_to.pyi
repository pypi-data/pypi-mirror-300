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

from .direction_option import direction_option as direction_option_cls
from .vector import vector as vector_cls
from .point import point as point_cls
from .axis_label import axis_label as axis_label_cls

class axis_to(Group):
    fluent_name = ...
    child_names = ...
    direction_option: direction_option_cls = ...
    vector: vector_cls = ...
    point: point_cls = ...
    axis_label: axis_label_cls = ...
