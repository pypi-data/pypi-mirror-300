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
from .injection_hole_child import injection_hole_child


class injection_hole(ListObject[injection_hole_child]):
    """
    'injection_hole' child.
    """

    fluent_name = "injection-hole"

    command_names = \
        ['list_properties']

    _child_classes = dict(
        list_properties=list_properties_cls,
    )

    child_object_type: injection_hole_child = injection_hole_child
    """
    child_object_type of injection_hole.
    """
    return_type = "<object object at 0x7fd93fba5250>"
