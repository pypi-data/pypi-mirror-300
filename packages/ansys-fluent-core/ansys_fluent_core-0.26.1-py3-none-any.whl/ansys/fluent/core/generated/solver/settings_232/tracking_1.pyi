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

from .high_res_tracking_enabled import high_res_tracking_enabled as high_res_tracking_enabled_cls
from .expert_options_1 import expert_options as expert_options_cls
from .high_res_tracking_options import high_res_tracking_options as high_res_tracking_options_cls
from .tracking_parameters import tracking_parameters as tracking_parameters_cls
from .track_in_absolute_frame import track_in_absolute_frame as track_in_absolute_frame_cls

class tracking(Group):
    fluent_name = ...
    child_names = ...
    high_res_tracking_enabled: high_res_tracking_enabled_cls = ...
    expert_options: expert_options_cls = ...
    high_res_tracking_options: high_res_tracking_options_cls = ...
    tracking_parameters: tracking_parameters_cls = ...
    track_in_absolute_frame: track_in_absolute_frame_cls = ...
    return_type = ...
