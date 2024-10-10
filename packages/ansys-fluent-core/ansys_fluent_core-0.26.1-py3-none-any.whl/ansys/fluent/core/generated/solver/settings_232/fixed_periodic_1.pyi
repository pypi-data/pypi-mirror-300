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

from .fixed_periodic import fixed_periodic as fixed_periodic_cls
from .fixed_periodic_type import fixed_periodic_type as fixed_periodic_type_cls
from .fixed_periodic_type_value import fixed_periodic_type_value as fixed_periodic_type_value_cls
from .times_step_periods import times_step_periods as times_step_periods_cls
from .total_period_run import total_period_run as total_period_run_cls

class fixed_periodic(Group):
    fluent_name = ...
    child_names = ...
    fixed_periodic: fixed_periodic_cls = ...
    fixed_periodic_type: fixed_periodic_type_cls = ...
    fixed_periodic_type_value: fixed_periodic_type_value_cls = ...
    times_step_periods: times_step_periods_cls = ...
    total_period_run: total_period_run_cls = ...
    return_type = ...
