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

from .list_properties_1 import list_properties as list_properties_cls
from .beach_dir_list_child import beach_dir_list_child


class beach_dir_list(ListObject[beach_dir_list_child]):
    """
    'beach_dir_list' child.
    """

    fluent_name = "beach-dir-list"

    command_names = \
        ['list_properties']

    _child_classes = dict(
        list_properties=list_properties_cls,
    )

    child_object_type: beach_dir_list_child = beach_dir_list_child
    """
    child_object_type of beach_dir_list.
    """
    return_type = "<object object at 0x7fe5ba6241a0>"
