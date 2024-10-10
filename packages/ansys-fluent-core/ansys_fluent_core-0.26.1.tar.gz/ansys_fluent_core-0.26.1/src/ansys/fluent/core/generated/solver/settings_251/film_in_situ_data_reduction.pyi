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

from .enabled_42 import enabled as enabled_cls
from .time_of_first_execution import time_of_first_execution as time_of_first_execution_cls
from .execution_time_interval import execution_time_interval as execution_time_interval_cls
from .per_face_parameters import per_face_parameters as per_face_parameters_cls

class film_in_situ_data_reduction(Group):
    fluent_name = ...
    child_names = ...
    enabled: enabled_cls = ...
    time_of_first_execution: time_of_first_execution_cls = ...
    execution_time_interval: execution_time_interval_cls = ...
    per_face_parameters: per_face_parameters_cls = ...
