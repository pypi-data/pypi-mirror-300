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
from .lines_child import lines_child


class lines(ListObject[lines_child]):
    """
    'lines' child.
    """

    fluent_name = "lines"

    command_names = \
        ['list_properties']

    _child_classes = dict(
        list_properties=list_properties_cls,
    )

    child_object_type: lines_child = lines_child
    """
    child_object_type of lines.
    """
    return_type = "<object object at 0x7fe5b8f46bb0>"
