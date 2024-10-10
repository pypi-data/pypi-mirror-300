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

from .schnerr_evap_coeff import schnerr_evap_coeff as schnerr_evap_coeff_cls
from .schnerr_cond_coeff import schnerr_cond_coeff as schnerr_cond_coeff_cls
from .max_vapor_pressure_ratio import max_vapor_pressure_ratio as max_vapor_pressure_ratio_cls
from .min_vapor_pressure import min_vapor_pressure as min_vapor_pressure_cls
from .display_clipped_pressure import display_clipped_pressure as display_clipped_pressure_cls
from .p_limit_method import p_limit_method as p_limit_method_cls
from .turbulent_diffusion import turbulent_diffusion as turbulent_diffusion_cls
from .old_treatment_for_turbulent_diffusion import old_treatment_for_turbulent_diffusion as old_treatment_for_turbulent_diffusion_cls

class cavitation(Group):
    fluent_name = ...
    child_names = ...
    schnerr_evap_coeff: schnerr_evap_coeff_cls = ...
    schnerr_cond_coeff: schnerr_cond_coeff_cls = ...
    max_vapor_pressure_ratio: max_vapor_pressure_ratio_cls = ...
    min_vapor_pressure: min_vapor_pressure_cls = ...
    display_clipped_pressure: display_clipped_pressure_cls = ...
    p_limit_method: p_limit_method_cls = ...
    turbulent_diffusion: turbulent_diffusion_cls = ...
    old_treatment_for_turbulent_diffusion: old_treatment_for_turbulent_diffusion_cls = ...
    return_type = ...
