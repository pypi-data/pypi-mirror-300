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

from .enable_solid_time_step import enable_solid_time_step as enable_solid_time_step_cls
from .choose_auto_time_stepping import choose_auto_time_stepping as choose_auto_time_stepping_cls
from .time_step_size_1 import time_step_size as time_step_size_cls

class solid_time_step_size(Group):
    fluent_name = ...
    child_names = ...
    enable_solid_time_step: enable_solid_time_step_cls = ...
    choose_auto_time_stepping: choose_auto_time_stepping_cls = ...
    time_step_size: time_step_size_cls = ...
    return_type = ...
