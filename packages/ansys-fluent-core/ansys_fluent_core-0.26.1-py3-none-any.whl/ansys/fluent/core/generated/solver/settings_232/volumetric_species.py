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
from .fluid_child import fluid_child


class volumetric_species(NamedObject[fluid_child], CreatableNamedObjectMixinOld[fluid_child]):
    """
    'volumetric_species' child.
    """

    fluent_name = "volumetric-species"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    _child_classes = dict(
        list=list_cls,
        list_properties=list_properties_cls,
        duplicate=duplicate_cls,
    )

    child_object_type: fluid_child = fluid_child
    """
    child_object_type of volumetric_species.
    """
    return_type = "<object object at 0x7fe5b9fa8cc0>"
