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

from .convergence_acceleration_type import convergence_acceleration_type as convergence_acceleration_type_cls
from .casm_cutoff_multiplier import casm_cutoff_multiplier as casm_cutoff_multiplier_cls

class convergence_acceleration_for_stretched_meshes(Group):
    fluent_name = ...
    child_names = ...
    convergence_acceleration_type: convergence_acceleration_type_cls = ...
    casm_cutoff_multiplier: casm_cutoff_multiplier_cls = ...
