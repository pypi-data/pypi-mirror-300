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

from .list_properties import list_properties as list_properties_cls
from .markers_child import markers_child


class markers(ListObject[markers_child]):
    """
    'markers' child.
    """

    fluent_name = "markers"

    command_names = \
        ['list_properties']

    _child_classes = dict(
        list_properties=list_properties_cls,
    )

    child_object_type: markers_child = markers_child
    """
    child_object_type of markers.
    """
    return_type = "<object object at 0x7fd93f8cc2d0>"
