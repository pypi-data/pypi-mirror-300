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

from .name_2 import name as name_cls
from .reference_frame import reference_frame as reference_frame_cls
from .point import point as point_cls
from .snap_method import snap_method as snap_method_cls

class point_surface_child(Group):
    fluent_name = ...
    child_names = ...
    name: name_cls = ...
    reference_frame: reference_frame_cls = ...
    point: point_cls = ...
    snap_method: snap_method_cls = ...
    return_type = ...
