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
from .mom_center import mom_center as mom_center_cls
from .mom_axis import mom_axis as mom_axis_cls
from .reference_frame import reference_frame as reference_frame_cls
from .zones_2 import zones as zones_cls
from .per_zone import per_zone as per_zone_cls
from .average_over import average_over as average_over_cls
from .retain_instantaneous_values import retain_instantaneous_values as retain_instantaneous_values_cls
from .report_output_type import report_output_type as report_output_type_cls
from .physics_1 import physics as physics_cls
from .geometry_5 import geometry as geometry_cls
from .create_output_parameter import create_output_parameter as create_output_parameter_cls

class moment_child(Group):
    fluent_name = ...
    child_names = ...
    name: name_cls = ...
    report_type: report_type_cls = ...
    mom_center: mom_center_cls = ...
    mom_axis: mom_axis_cls = ...
    reference_frame: reference_frame_cls = ...
    zones: zones_cls = ...
    per_zone: per_zone_cls = ...
    average_over: average_over_cls = ...
    retain_instantaneous_values: retain_instantaneous_values_cls = ...
    report_output_type: report_output_type_cls = ...
    physics: physics_cls = ...
    geometry: geometry_cls = ...
    command_names = ...

    def create_output_parameter(self, ):
        """
        'create_output_parameter' command.
        """

    return_type = ...
