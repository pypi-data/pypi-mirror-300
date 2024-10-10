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

from .name_2 import name as name_cls
from .zone_ids import zone_ids as zone_ids_cls
from .retain_instantaneous_values import retain_instantaneous_values as retain_instantaneous_values_cls
from .old_props import old_props as old_props_cls
from .zone_names_1 import zone_names as zone_names_cls
from .zone_list import zone_list as zone_list_cls
from .average_over import average_over as average_over_cls
from .per_zone import per_zone as per_zone_cls

class mesh_child(Group):
    """
    'child_object_type' of mesh.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'zone_ids', 'retain_instantaneous_values', 'old_props',
         'zone_names', 'zone_list', 'average_over', 'per_zone']

    _child_classes = dict(
        name=name_cls,
        zone_ids=zone_ids_cls,
        retain_instantaneous_values=retain_instantaneous_values_cls,
        old_props=old_props_cls,
        zone_names=zone_names_cls,
        zone_list=zone_list_cls,
        average_over=average_over_cls,
        per_zone=per_zone_cls,
    )

    return_type = "<object object at 0x7fe5b9059210>"
