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

from .monitor import monitor as monitor_cls
from .normalization_factor import normalization_factor as normalization_factor_cls
from .check_convergence import check_convergence as check_convergence_cls
from .absolute_criteria import absolute_criteria as absolute_criteria_cls
from .relative_criteria import relative_criteria as relative_criteria_cls

class equations_child(Group):
    fluent_name = ...
    child_names = ...
    monitor: monitor_cls = ...
    normalization_factor: normalization_factor_cls = ...
    check_convergence: check_convergence_cls = ...
    absolute_criteria: absolute_criteria_cls = ...
    relative_criteria: relative_criteria_cls = ...
    return_type = ...
