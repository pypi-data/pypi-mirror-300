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

from .axis_direction_component_child import axis_direction_component_child


class origin_position_of_rotation_axis(ListObject[axis_direction_component_child]):
    """
    'origin_position_of_rotation_axis' child.
    """

    fluent_name = "origin-position-of-rotation-axis"

    child_object_type: axis_direction_component_child = axis_direction_component_child
    """
    child_object_type of origin_position_of_rotation_axis.
    """
    return_type = "<object object at 0x7f82c5a97560>"
