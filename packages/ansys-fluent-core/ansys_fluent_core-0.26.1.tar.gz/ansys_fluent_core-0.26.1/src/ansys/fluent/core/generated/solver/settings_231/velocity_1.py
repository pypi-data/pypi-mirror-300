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


class velocity(ListObject[child_object_type_child]):
    """
    'velocity' child.
    """

    fluent_name = "velocity"

    child_object_type: child_object_type_child = child_object_type_child
    """
    child_object_type of velocity.
    """
    return_type = "<object object at 0x7ff9d0e52620>"
