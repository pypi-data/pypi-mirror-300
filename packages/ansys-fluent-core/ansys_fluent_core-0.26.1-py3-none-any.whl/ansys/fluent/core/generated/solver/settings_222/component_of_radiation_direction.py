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


class component_of_radiation_direction(ListObject[child_object_type_child]):
    """
    'component_of_radiation_direction' child.
    """

    fluent_name = "component-of-radiation-direction"

    child_object_type: child_object_type_child = child_object_type_child
    """
    child_object_type of component_of_radiation_direction.
    """
    return_type = "<object object at 0x7f82c5a96060>"
