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

from .name import name as name_cls
from .report_type import report_type as report_type_cls
from .field import field as field_cls
from .cell_zones_4 import cell_zones as cell_zones_cls
from .per_zone import per_zone as per_zone_cls
from .average_over import average_over as average_over_cls
from .retain_instantaneous_values import retain_instantaneous_values as retain_instantaneous_values_cls
from .phase_31 import phase as phase_cls
from .physics_1 import physics as physics_cls
from .geometry_7 import geometry as geometry_cls
from .output_parameter_1 import output_parameter as output_parameter_cls
from .create_output_parameter import create_output_parameter as create_output_parameter_cls

class volume_child(Group):
    fluent_name = ...
    child_names = ...
    name: name_cls = ...
    report_type: report_type_cls = ...
    field: field_cls = ...
    cell_zones: cell_zones_cls = ...
    per_zone: per_zone_cls = ...
    average_over: average_over_cls = ...
    retain_instantaneous_values: retain_instantaneous_values_cls = ...
    phase: phase_cls = ...
    physics: physics_cls = ...
    geometry: geometry_cls = ...
    output_parameter: output_parameter_cls = ...
    command_names = ...

    def create_output_parameter(self, ):
        """
        Option to make report definition available as an output parameter.
        """

