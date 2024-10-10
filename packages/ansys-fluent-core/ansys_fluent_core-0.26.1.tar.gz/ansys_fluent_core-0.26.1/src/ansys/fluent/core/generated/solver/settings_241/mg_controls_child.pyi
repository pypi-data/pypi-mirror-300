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

from .cycle_type import cycle_type as cycle_type_cls
from .termination_criteria import termination_criteria as termination_criteria_cls
from .residual_reduction_tolerance import residual_reduction_tolerance as residual_reduction_tolerance_cls
from .method_8 import method as method_cls
from .stabilization import stabilization as stabilization_cls

class mg_controls_child(Group):
    fluent_name = ...
    child_names = ...
    cycle_type: cycle_type_cls = ...
    termination_criteria: termination_criteria_cls = ...
    residual_reduction_tolerance: residual_reduction_tolerance_cls = ...
    method: method_cls = ...
    stabilization: stabilization_cls = ...
    return_type = ...
