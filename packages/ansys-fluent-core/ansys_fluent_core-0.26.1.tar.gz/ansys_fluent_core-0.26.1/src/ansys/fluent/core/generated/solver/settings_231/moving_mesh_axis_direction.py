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

from .child_object_type_child_1 import child_object_type_child


class moving_mesh_axis_direction(ListObject[child_object_type_child]):
    """
    'moving_mesh_axis_direction' child.
    """

    fluent_name = "moving-mesh-axis-direction"

    child_object_type: child_object_type_child = child_object_type_child
    """
    child_object_type of moving_mesh_axis_direction.
    """
    return_type = "<object object at 0x7ff9d17197b0>"
