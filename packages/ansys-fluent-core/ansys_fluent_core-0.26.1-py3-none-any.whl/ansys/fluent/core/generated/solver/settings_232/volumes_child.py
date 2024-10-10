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

from .type_3 import type as type_cls
from .boundaries import boundaries as boundaries_cls
from .locations import locations as locations_cls

class volumes_child(Group):
    """
    'child_object_type' of volumes.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['type', 'boundaries', 'locations']

    _child_classes = dict(
        type=type_cls,
        boundaries=boundaries_cls,
        locations=locations_cls,
    )

    return_type = "<object object at 0x7fe5b915e920>"
