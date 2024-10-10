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

from .enabled_2 import enabled as enabled_cls
from .global_courant_number import global_courant_number as global_courant_number_cls
from .initial_time_step_size import initial_time_step_size as initial_time_step_size_cls
from .fixed_time_step_size import fixed_time_step_size as fixed_time_step_size_cls
from .min_time_step_size import min_time_step_size as min_time_step_size_cls
from .max_time_step_size import max_time_step_size as max_time_step_size_cls
from .min_step_change_factor import min_step_change_factor as min_step_change_factor_cls
from .max_step_change_factor import max_step_change_factor as max_step_change_factor_cls
from .update_interval import update_interval as update_interval_cls

class mp_specific_time_stepping(Group):
    fluent_name = ...
    child_names = ...
    enabled: enabled_cls = ...
    global_courant_number: global_courant_number_cls = ...
    initial_time_step_size: initial_time_step_size_cls = ...
    fixed_time_step_size: fixed_time_step_size_cls = ...
    min_time_step_size: min_time_step_size_cls = ...
    max_time_step_size: max_time_step_size_cls = ...
    min_step_change_factor: min_step_change_factor_cls = ...
    max_step_change_factor: max_step_change_factor_cls = ...
    update_interval: update_interval_cls = ...
    return_type = ...
