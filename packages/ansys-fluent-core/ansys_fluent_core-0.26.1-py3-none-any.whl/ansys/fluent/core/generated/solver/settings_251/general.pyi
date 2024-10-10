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

from .solver import solver as solver_cls
from .adjust_solver_defaults_based_on_setup import adjust_solver_defaults_based_on_setup as adjust_solver_defaults_based_on_setup_cls
from .operating_conditions import operating_conditions as operating_conditions_cls
from .units import units as units_cls

class general(Group):
    fluent_name = ...
    child_names = ...
    solver: solver_cls = ...
    adjust_solver_defaults_based_on_setup: adjust_solver_defaults_based_on_setup_cls = ...
    operating_conditions: operating_conditions_cls = ...
    units: units_cls = ...
