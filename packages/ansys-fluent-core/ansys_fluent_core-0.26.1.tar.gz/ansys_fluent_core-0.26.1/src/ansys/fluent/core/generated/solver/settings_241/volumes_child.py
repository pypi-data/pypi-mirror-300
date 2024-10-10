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

from .name import name as name_cls
from .type_4 import type as type_cls
from .boundaries import boundaries as boundaries_cls
from .locations import locations as locations_cls

class volumes_child(Group):
    """
    'child_object_type' of volumes.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'type', 'boundaries', 'locations']

    _child_classes = dict(
        name=name_cls,
        type=type_cls,
        boundaries=boundaries_cls,
        locations=locations_cls,
    )

    return_type = "<object object at 0x7fd93fba6d40>"
