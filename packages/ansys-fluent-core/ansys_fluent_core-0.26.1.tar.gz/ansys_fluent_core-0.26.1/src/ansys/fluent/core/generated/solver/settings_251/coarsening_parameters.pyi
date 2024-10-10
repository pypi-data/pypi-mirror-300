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

from .global_dt_coarsen_by_interval import global_dt_coarsen_by_interval as global_dt_coarsen_by_interval_cls
from .coarsen_by_interval import coarsen_by_interval as coarsen_by_interval_cls

class coarsening_parameters(Group):
    fluent_name = ...
    child_names = ...
    global_dt_coarsen_by_interval: global_dt_coarsen_by_interval_cls = ...
    coarsen_by_interval: coarsen_by_interval_cls = ...
