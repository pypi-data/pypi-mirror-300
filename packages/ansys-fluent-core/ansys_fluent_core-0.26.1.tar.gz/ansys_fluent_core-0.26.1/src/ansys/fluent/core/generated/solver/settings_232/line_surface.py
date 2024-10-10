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
from .line_surface_child import line_surface_child


class line_surface(NamedObject[line_surface_child], CreatableNamedObjectMixinOld[line_surface_child]):
    """
    'line_surface' child.
    """

    fluent_name = "line-surface"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    _child_classes = dict(
        list=list_cls,
        list_properties=list_properties_cls,
        duplicate=duplicate_cls,
    )

    child_object_type: line_surface_child = line_surface_child
    """
    child_object_type of line_surface.
    """
    return_type = "<object object at 0x7fe5b8f44e50>"
