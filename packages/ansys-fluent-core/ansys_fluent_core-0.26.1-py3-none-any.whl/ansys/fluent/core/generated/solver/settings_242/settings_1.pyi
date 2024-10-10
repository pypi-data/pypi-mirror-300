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

from .degassing_verbosity import degassing_verbosity as degassing_verbosity_cls
from .mass_flow import mass_flow as mass_flow_cls
from .pressure_outlet_1 import pressure_outlet as pressure_outlet_cls
from .pressure_far_field_1 import pressure_far_field as pressure_far_field_cls
from .physical_velocity_porous_formulation import physical_velocity_porous_formulation as physical_velocity_porous_formulation_cls
from .target_mass_flow_rate_settings import target_mass_flow_rate_settings as target_mass_flow_rate_settings_cls
from .advanced_2 import advanced as advanced_cls
from .detect_boundary_advection import detect_boundary_advection as detect_boundary_advection_cls

class settings(Group):
    fluent_name = ...
    child_names = ...
    degassing_verbosity: degassing_verbosity_cls = ...
    mass_flow: mass_flow_cls = ...
    pressure_outlet: pressure_outlet_cls = ...
    pressure_far_field: pressure_far_field_cls = ...
    physical_velocity_porous_formulation: physical_velocity_porous_formulation_cls = ...
    target_mass_flow_rate_settings: target_mass_flow_rate_settings_cls = ...
    advanced: advanced_cls = ...
    command_names = ...

    def detect_boundary_advection(self, ):
        """
        Detect and set boundary advection at solid walls.
        """

