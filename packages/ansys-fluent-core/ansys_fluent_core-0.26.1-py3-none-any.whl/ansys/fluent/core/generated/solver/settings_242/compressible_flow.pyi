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

from .enhanced_numerics import enhanced_numerics as enhanced_numerics_cls
from .alternate_bc_formulation import alternate_bc_formulation as alternate_bc_formulation_cls
from .analytical_thermodynamic_derivatives import analytical_thermodynamic_derivatives as analytical_thermodynamic_derivatives_cls

class compressible_flow(Group):
    fluent_name = ...
    child_names = ...
    enhanced_numerics: enhanced_numerics_cls = ...
    alternate_bc_formulation: alternate_bc_formulation_cls = ...
    analytical_thermodynamic_derivatives: analytical_thermodynamic_derivatives_cls = ...
