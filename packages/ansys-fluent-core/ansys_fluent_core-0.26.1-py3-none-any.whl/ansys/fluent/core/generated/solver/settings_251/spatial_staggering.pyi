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

from .enabled_16 import enabled as enabled_cls
from .radius import radius as radius_cls
from .only_in_plane import only_in_plane as only_in_plane_cls

class spatial_staggering(Group):
    fluent_name = ...
    child_names = ...
    enabled: enabled_cls = ...
    radius: radius_cls = ...
    only_in_plane: only_in_plane_cls = ...
