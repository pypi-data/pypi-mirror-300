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

from .enabled_12 import enabled as enabled_cls
from .calendar_time import calendar_time as calendar_time_cls
from .cycle_number import cycle_number as cycle_number_cls
from .operation_temperature import operation_temperature as operation_temperature_cls
from .calendar_life_params import calendar_life_params as calendar_life_params_cls
from .cycle_life_table import cycle_life_table as cycle_life_table_cls

class life_model(Group):
    fluent_name = ...
    child_names = ...
    enabled: enabled_cls = ...
    calendar_time: calendar_time_cls = ...
    cycle_number: cycle_number_cls = ...
    operation_temperature: operation_temperature_cls = ...
    calendar_life_params: calendar_life_params_cls = ...
    cycle_life_table: cycle_life_table_cls = ...
    return_type = ...
