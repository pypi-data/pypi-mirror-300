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

from .list_properties import list_properties as list_properties_cls
from .resize import resize as resize_cls
from .reference_frame_velocity_child import reference_frame_velocity_child


class solid_motion_axis_origin(ListObject[reference_frame_velocity_child]):
    """
    Set solid motion axis origin components.
    """

    fluent_name = "solid-motion-axis-origin"

    command_names = \
        ['list_properties', 'resize']

    _child_classes = dict(
        list_properties=list_properties_cls,
        resize=resize_cls,
    )

    child_object_type: reference_frame_velocity_child = reference_frame_velocity_child
    """
    child_object_type of solid_motion_axis_origin.
    """
