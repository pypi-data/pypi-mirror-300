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


class axis_origin_component(ListObject[axis_direction_component_child]):
    """
    'axis_origin_component' child.
    """

    fluent_name = "axis-origin-component"

    child_object_type: axis_direction_component_child = axis_direction_component_child
    """
    child_object_type of axis_origin_component.
    """
    return_type = "<object object at 0x7f82c6907680>"
