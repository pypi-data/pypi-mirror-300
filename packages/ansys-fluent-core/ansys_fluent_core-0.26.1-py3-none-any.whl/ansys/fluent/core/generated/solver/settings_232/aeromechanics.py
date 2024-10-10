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
from .aeromechanics_child import aeromechanics_child


class aeromechanics(NamedObject[aeromechanics_child], CreatableNamedObjectMixinOld[aeromechanics_child]):
    """
    'aeromechanics' child.
    """

    fluent_name = "aeromechanics"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    _child_classes = dict(
        list=list_cls,
        list_properties=list_properties_cls,
        duplicate=duplicate_cls,
    )

    child_object_type: aeromechanics_child = aeromechanics_child
    """
    child_object_type of aeromechanics.
    """
    return_type = "<object object at 0x7fe5b905a1a0>"
