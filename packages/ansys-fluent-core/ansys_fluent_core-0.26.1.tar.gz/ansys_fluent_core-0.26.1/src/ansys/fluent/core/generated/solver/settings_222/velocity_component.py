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

from .child_object_type_child import child_object_type_child


class velocity_component(ListObject[child_object_type_child]):
    """
    'velocity_component' child.
    """

    fluent_name = "velocity-component"

    child_object_type: child_object_type_child = child_object_type_child
    """
    child_object_type of velocity_component.
    """
    return_type = "<object object at 0x7f82c5cd8f70>"
