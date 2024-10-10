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

from .list import list as list_cls
from .list_properties import list_properties as list_properties_cls
from .duplicate import duplicate as duplicate_cls
from .child_object_type_child_1 import child_object_type_child


class fixes(NamedObject[child_object_type_child], _NonCreatableNamedObjectMixin[child_object_type_child]):
    """
    'fixes' child.
    """

    fluent_name = "fixes"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    _child_classes = dict(
        list=list_cls,
        list_properties=list_properties_cls,
        duplicate=duplicate_cls,
    )

    child_object_type: child_object_type_child = child_object_type_child
    """
    child_object_type of fixes.
    """
    return_type = "<object object at 0x7fe5ba24a2b0>"
