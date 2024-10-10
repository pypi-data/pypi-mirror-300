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
from .phase_57 import phase as phase_cls
from .boundaries import boundaries as boundaries_cls
from .location_2 import location as location_cls
from .split import split as split_cls

class solid_child(Group):
    """
    'child_object_type' of solid.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'type', 'phase', 'boundaries', 'location']

    command_names = \
        ['split']

    _child_classes = dict(
        name=name_cls,
        type=type_cls,
        phase=phase_cls,
        boundaries=boundaries_cls,
        location=location_cls,
        split=split_cls,
    )

