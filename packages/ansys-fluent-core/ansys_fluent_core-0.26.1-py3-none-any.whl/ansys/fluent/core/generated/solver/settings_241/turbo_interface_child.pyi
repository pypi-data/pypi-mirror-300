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

from .name import name as name_cls
from .zone1_1 import zone1 as zone1_cls
from .zone2_1 import zone2 as zone2_cls
from .pitch_change_types import pitch_change_types as pitch_change_types_cls
from .mixing_plane import mixing_plane as mixing_plane_cls
from .turbo_non_overlap import turbo_non_overlap as turbo_non_overlap_cls

class turbo_interface_child(Group):
    fluent_name = ...
    child_names = ...
    name: name_cls = ...
    zone1: zone1_cls = ...
    zone2: zone2_cls = ...
    pitch_change_types: pitch_change_types_cls = ...
    mixing_plane: mixing_plane_cls = ...
    turbo_non_overlap: turbo_non_overlap_cls = ...
    return_type = ...
