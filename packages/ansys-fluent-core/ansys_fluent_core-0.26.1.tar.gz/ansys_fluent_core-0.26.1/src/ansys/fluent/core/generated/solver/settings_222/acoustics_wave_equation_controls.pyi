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

from .expert import expert as expert_cls
from .relative_convergence_criterion import relative_convergence_criterion as relative_convergence_criterion_cls
from .max_iterations_per_timestep import max_iterations_per_timestep as max_iterations_per_timestep_cls

class acoustics_wave_equation_controls(Group):
    fluent_name = ...
    child_names = ...
    expert: expert_cls = ...
    relative_convergence_criterion: relative_convergence_criterion_cls = ...
    max_iterations_per_timestep: max_iterations_per_timestep_cls = ...
    return_type = ...
