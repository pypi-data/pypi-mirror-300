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
from .phase_12 import phase as phase_cls
from .thermal_bc import thermal_bc as thermal_bc_cls
from .temperature_1 import temperature as temperature_cls
from .q import q as q_cls

class network_end_child(Group):
    """
    'child_object_type' of network_end.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'phase', 'thermal_bc', 'temperature', 'q']

    _child_classes = dict(
        name=name_cls,
        phase=phase_cls,
        thermal_bc=thermal_bc_cls,
        temperature=temperature_cls,
        q=q_cls,
    )

    return_type = "<object object at 0x7fd94d9ca150>"
