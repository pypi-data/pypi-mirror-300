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
from .motion import motion as motion_cls
from .parent_ref_frame import parent_ref_frame as parent_ref_frame_cls
from .initial_state import initial_state as initial_state_cls
from .current_state import current_state as current_state_cls
from .display_state import display_state as display_state_cls

class reference_frames_child(Group):
    fluent_name = ...
    child_names = ...
    name: name_cls = ...
    motion: motion_cls = ...
    parent_ref_frame: parent_ref_frame_cls = ...
    initial_state: initial_state_cls = ...
    current_state: current_state_cls = ...
    display_state: display_state_cls = ...
