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

from .parallel_verbosity_level import parallel_verbosity_level as parallel_verbosity_level_cls
from .crossover_tolerance import crossover_tolerance as crossover_tolerance_cls

class expert(Group):
    fluent_name = ...
    child_names = ...
    parallel_verbosity_level: parallel_verbosity_level_cls = ...
    crossover_tolerance: crossover_tolerance_cls = ...
