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

from .multi_grid import multi_grid as multi_grid_cls
from .multi_stage import multi_stage as multi_stage_cls
from .expert_4 import expert as expert_cls
from .fast_transient_settings import fast_transient_settings as fast_transient_settings_cls
from .relaxation_method_1 import relaxation_method as relaxation_method_cls
from .correction_tolerance import correction_tolerance as correction_tolerance_cls
from .anisotropic_solid_heat_transfer import anisotropic_solid_heat_transfer as anisotropic_solid_heat_transfer_cls

class advanced(Group):
    fluent_name = ...
    child_names = ...
    multi_grid: multi_grid_cls = ...
    multi_stage: multi_stage_cls = ...
    expert: expert_cls = ...
    fast_transient_settings: fast_transient_settings_cls = ...
    relaxation_method: relaxation_method_cls = ...
    correction_tolerance: correction_tolerance_cls = ...
    anisotropic_solid_heat_transfer: anisotropic_solid_heat_transfer_cls = ...
    return_type = ...
