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


class uds(NamedObject[child_object_type_child], _NonCreatableNamedObjectMixin[child_object_type_child]):
    """
    'uds' child.
    """

    fluent_name = "uds"

    child_object_type: child_object_type_child = child_object_type_child
    """
    child_object_type of uds.
    """
    return_type = "<object object at 0x7ff9d15597c0>"
