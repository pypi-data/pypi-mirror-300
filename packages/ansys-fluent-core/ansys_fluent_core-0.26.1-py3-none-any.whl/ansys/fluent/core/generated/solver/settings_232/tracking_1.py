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

from .high_res_tracking_enabled import high_res_tracking_enabled as high_res_tracking_enabled_cls
from .expert_options_1 import expert_options as expert_options_cls
from .high_res_tracking_options import high_res_tracking_options as high_res_tracking_options_cls
from .tracking_parameters import tracking_parameters as tracking_parameters_cls
from .track_in_absolute_frame import track_in_absolute_frame as track_in_absolute_frame_cls

class tracking(Group):
    """
    Main menu to control the time integration of the particle trajectory equations.
    """

    fluent_name = "tracking"

    child_names = \
        ['high_res_tracking_enabled', 'expert_options',
         'high_res_tracking_options', 'tracking_parameters',
         'track_in_absolute_frame']

    _child_classes = dict(
        high_res_tracking_enabled=high_res_tracking_enabled_cls,
        expert_options=expert_options_cls,
        high_res_tracking_options=high_res_tracking_options_cls,
        tracking_parameters=tracking_parameters_cls,
        track_in_absolute_frame=track_in_absolute_frame_cls,
    )

    return_type = "<object object at 0x7fe5b9e4d8b0>"
