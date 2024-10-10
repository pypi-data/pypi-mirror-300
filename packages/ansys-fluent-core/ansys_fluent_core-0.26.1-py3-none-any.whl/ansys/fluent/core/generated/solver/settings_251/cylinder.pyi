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

from .axis_begin import axis_begin as axis_begin_cls
from .axis_end import axis_end as axis_end_cls
from .radius_1 import radius as radius_cls
from .inside import inside as inside_cls

class cylinder(Group):
    fluent_name = ...
    child_names = ...
    axis_begin: axis_begin_cls = ...
    axis_end: axis_end_cls = ...
    radius: radius_cls = ...
    inside: inside_cls = ...
