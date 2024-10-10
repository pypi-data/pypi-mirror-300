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

from .n_smooth_for_interfacial_regims import n_smooth_for_interfacial_regims as n_smooth_for_interfacial_regims_cls
from .sm_relax_factor import sm_relax_factor as sm_relax_factor_cls
from .viscous_func_options import viscous_func_options as viscous_func_options_cls
from .density_func_options import density_func_options as density_func_options_cls
from .exponent_smoothing_func import exponent_smoothing_func as exponent_smoothing_func_cls
from .exponent_density_func import exponent_density_func as exponent_density_func_cls
from .boundry_treatment import boundry_treatment as boundry_treatment_cls
from .near_wall_treatment_1 import near_wall_treatment as near_wall_treatment_cls

class interfacial_artificial_viscosity(Group):
    fluent_name = ...
    child_names = ...
    n_smooth_for_interfacial_regims: n_smooth_for_interfacial_regims_cls = ...
    sm_relax_factor: sm_relax_factor_cls = ...
    viscous_func_options: viscous_func_options_cls = ...
    density_func_options: density_func_options_cls = ...
    exponent_smoothing_func: exponent_smoothing_func_cls = ...
    exponent_density_func: exponent_density_func_cls = ...
    boundry_treatment: boundry_treatment_cls = ...
    near_wall_treatment: near_wall_treatment_cls = ...
