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

from .porous_jump_turb_wall_treatment import porous_jump_turb_wall_treatment as porous_jump_turb_wall_treatment_cls
from .reverse_fan_direction import reverse_fan_direction as reverse_fan_direction_cls
from .profile_specification_of_pressure_jump import profile_specification_of_pressure_jump as profile_specification_of_pressure_jump_cls
from .pressure_jump import pressure_jump as pressure_jump_cls
from .pressure_jump_profile import pressure_jump_profile as pressure_jump_profile_cls
from .limit_polynomial_velocity_range import limit_polynomial_velocity_range as limit_polynomial_velocity_range_cls
from .min_velocity import min_velocity as min_velocity_cls
from .max_velocity import max_velocity as max_velocity_cls
from .strength import strength as strength_cls
from .cal_pressure_jump_from_avg_conditions import cal_pressure_jump_from_avg_conditions as cal_pressure_jump_from_avg_conditions_cls
from .new_fan_definition import new_fan_definition as new_fan_definition_cls

class pressure_jump_specification(Group):
    fluent_name = ...
    child_names = ...
    porous_jump_turb_wall_treatment: porous_jump_turb_wall_treatment_cls = ...
    reverse_fan_direction: reverse_fan_direction_cls = ...
    profile_specification_of_pressure_jump: profile_specification_of_pressure_jump_cls = ...
    pressure_jump: pressure_jump_cls = ...
    pressure_jump_profile: pressure_jump_profile_cls = ...
    limit_polynomial_velocity_range: limit_polynomial_velocity_range_cls = ...
    min_velocity: min_velocity_cls = ...
    max_velocity: max_velocity_cls = ...
    strength: strength_cls = ...
    cal_pressure_jump_from_avg_conditions: cal_pressure_jump_from_avg_conditions_cls = ...
    new_fan_definition: new_fan_definition_cls = ...
