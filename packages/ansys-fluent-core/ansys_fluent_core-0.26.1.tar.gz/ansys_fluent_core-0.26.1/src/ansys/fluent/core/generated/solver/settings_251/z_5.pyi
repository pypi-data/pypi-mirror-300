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

from .points import points as points_cls
from .motion_enabled import motion_enabled as motion_enabled_cls
from .invariant import invariant as invariant_cls
from .invariant_expert_controls import invariant_expert_controls as invariant_expert_controls_cls
from .symmetric import symmetric as symmetric_cls
from .custom_plane import custom_plane as custom_plane_cls
from .periodicity_1 import periodicity as periodicity_cls

class z(Group):
    fluent_name = ...
    child_names = ...
    points: points_cls = ...
    motion_enabled: motion_enabled_cls = ...
    invariant: invariant_cls = ...
    invariant_expert_controls: invariant_expert_controls_cls = ...
    symmetric: symmetric_cls = ...
    custom_plane: custom_plane_cls = ...
    periodicity: periodicity_cls = ...
