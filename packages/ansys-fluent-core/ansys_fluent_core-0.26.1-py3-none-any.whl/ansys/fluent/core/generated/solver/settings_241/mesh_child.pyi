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
from .per_zone import per_zone as per_zone_cls
from .average_over import average_over as average_over_cls
from .retain_instantaneous_values import retain_instantaneous_values as retain_instantaneous_values_cls
from .cell_zones_3 import cell_zones as cell_zones_cls
from .face_zones import face_zones as face_zones_cls
from .create_output_parameter import create_output_parameter as create_output_parameter_cls

class mesh_child(Group):
    fluent_name = ...
    child_names = ...
    name: name_cls = ...
    report_type: report_type_cls = ...
    per_zone: per_zone_cls = ...
    average_over: average_over_cls = ...
    retain_instantaneous_values: retain_instantaneous_values_cls = ...
    cell_zones: cell_zones_cls = ...
    face_zones: face_zones_cls = ...
    command_names = ...

    def create_output_parameter(self, ):
        """
        'create_output_parameter' command.
        """

    return_type = ...
