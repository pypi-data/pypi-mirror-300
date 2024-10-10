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

from .enabled_18 import enabled as enabled_cls
from .user_defined_timestep import user_defined_timestep as user_defined_timestep_cls
from .error_tolerance import error_tolerance as error_tolerance_cls
from .time_end import time_end as time_end_cls
from .min_time_step import min_time_step as min_time_step_cls
from .max_time_step import max_time_step as max_time_step_cls
from .min_step_change_factor import min_step_change_factor as min_step_change_factor_cls
from .max_step_change_factor import max_step_change_factor as max_step_change_factor_cls
from .fixed_time_step_count import fixed_time_step_count as fixed_time_step_count_cls

class adaptive_time_stepping(Group):
    fluent_name = ...
    child_names = ...
    enabled: enabled_cls = ...
    user_defined_timestep: user_defined_timestep_cls = ...
    error_tolerance: error_tolerance_cls = ...
    time_end: time_end_cls = ...
    min_time_step: min_time_step_cls = ...
    max_time_step: max_time_step_cls = ...
    min_step_change_factor: min_step_change_factor_cls = ...
    max_step_change_factor: max_step_change_factor_cls = ...
    fixed_time_step_count: fixed_time_step_count_cls = ...
    return_type = ...
