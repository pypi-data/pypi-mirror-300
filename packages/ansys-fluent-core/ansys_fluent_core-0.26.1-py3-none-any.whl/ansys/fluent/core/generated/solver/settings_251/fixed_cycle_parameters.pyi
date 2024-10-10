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

from .global_dt_post_sweeps import global_dt_post_sweeps as global_dt_post_sweeps_cls
from .post_sweeps import post_sweeps as post_sweeps_cls
from .global_dt_max_cycle import global_dt_max_cycle as global_dt_max_cycle_cls
from .max_cycle import max_cycle as max_cycle_cls

class fixed_cycle_parameters(Group):
    fluent_name = ...
    child_names = ...
    global_dt_post_sweeps: global_dt_post_sweeps_cls = ...
    post_sweeps: post_sweeps_cls = ...
    global_dt_max_cycle: global_dt_max_cycle_cls = ...
    max_cycle: max_cycle_cls = ...
