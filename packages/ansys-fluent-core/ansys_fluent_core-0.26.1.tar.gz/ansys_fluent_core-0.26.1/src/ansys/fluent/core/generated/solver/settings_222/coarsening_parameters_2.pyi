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

from .max_coarse_levels_2 import max_coarse_levels as max_coarse_levels_cls
from .coarsen_by_interval_2 import coarsen_by_interval as coarsen_by_interval_cls

class coarsening_parameters(Group):
    fluent_name = ...
    child_names = ...
    max_coarse_levels: max_coarse_levels_cls = ...
    coarsen_by_interval: coarsen_by_interval_cls = ...
    return_type = ...
