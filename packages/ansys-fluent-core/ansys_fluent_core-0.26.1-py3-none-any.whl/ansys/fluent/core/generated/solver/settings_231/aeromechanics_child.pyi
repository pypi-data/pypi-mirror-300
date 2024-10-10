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

from typing import Union, List, Tuple

from .report_type import report_type as report_type_cls
from .realcomponent import realcomponent as realcomponent_cls
from .nodal_diameters import nodal_diameters as nodal_diameters_cls
from .normalization import normalization as normalization_cls
from .integrate_over import integrate_over as integrate_over_cls
from .average_over import average_over as average_over_cls
from .per_zone import per_zone as per_zone_cls
from .old_props import old_props as old_props_cls
from .thread_names import thread_names as thread_names_cls
from .thread_ids import thread_ids as thread_ids_cls

class aeromechanics_child(Group):
    fluent_name = ...
    child_names = ...
    report_type: report_type_cls = ...
    realcomponent: realcomponent_cls = ...
    nodal_diameters: nodal_diameters_cls = ...
    normalization: normalization_cls = ...
    integrate_over: integrate_over_cls = ...
    average_over: average_over_cls = ...
    per_zone: per_zone_cls = ...
    old_props: old_props_cls = ...
    thread_names: thread_names_cls = ...
    thread_ids: thread_ids_cls = ...
    return_type = ...
