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
from .zones_2 import zones as zones_cls
from .per_zone import per_zone as per_zone_cls
from .nodal_diameters import nodal_diameters as nodal_diameters_cls
from .average_over import average_over as average_over_cls
from .integrate_over import integrate_over as integrate_over_cls
from .normalization import normalization as normalization_cls
from .realcomponent import realcomponent as realcomponent_cls
from .create_output_parameter import create_output_parameter as create_output_parameter_cls

class aeromechanics_child(Group):
    fluent_name = ...
    child_names = ...
    name: name_cls = ...
    report_type: report_type_cls = ...
    zones: zones_cls = ...
    per_zone: per_zone_cls = ...
    nodal_diameters: nodal_diameters_cls = ...
    average_over: average_over_cls = ...
    integrate_over: integrate_over_cls = ...
    normalization: normalization_cls = ...
    realcomponent: realcomponent_cls = ...
    command_names = ...

    def create_output_parameter(self, ):
        """
        'create_output_parameter' command.
        """

    return_type = ...
