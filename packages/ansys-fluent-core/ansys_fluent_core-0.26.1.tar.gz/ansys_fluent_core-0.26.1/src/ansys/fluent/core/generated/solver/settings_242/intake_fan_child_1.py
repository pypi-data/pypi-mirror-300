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
from .type_5 import type as type_cls
from .location_2 import location as location_cls
from .phase_37 import phase as phase_cls

class intake_fan_child(Group):
    """
    'child_object_type' of intake_fan.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'type', 'location', 'phase']

    _child_classes = dict(
        name=name_cls,
        type=type_cls,
        location=location_cls,
        phase=phase_cls,
    )

