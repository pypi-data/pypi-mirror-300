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

from .number_of_recycled_modes import number_of_recycled_modes as number_of_recycled_modes_cls
from .amg_iterations import amg_iterations as amg_iterations_cls

class expert_controls(Group):
    fluent_name = ...
    child_names = ...
    number_of_recycled_modes: number_of_recycled_modes_cls = ...
    amg_iterations: amg_iterations_cls = ...
