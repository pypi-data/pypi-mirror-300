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

from .critical_temperature_option import critical_temperature_option as critical_temperature_option_cls
from .critical_temperature_factor import critical_temperature_factor as critical_temperature_factor_cls
from .critical_temperature_offset import critical_temperature_offset as critical_temperature_offset_cls
from .upper_deposition_limit_offset import upper_deposition_limit_offset as upper_deposition_limit_offset_cls
from .deposition_delta_t import deposition_delta_t as deposition_delta_t_cls
from .laplace_number_constant import laplace_number_constant as laplace_number_constant_cls
from .partial_evaporation_ratio import partial_evaporation_ratio as partial_evaporation_ratio_cls

class regime_parameters(Group):
    fluent_name = ...
    child_names = ...
    critical_temperature_option: critical_temperature_option_cls = ...
    critical_temperature_factor: critical_temperature_factor_cls = ...
    critical_temperature_offset: critical_temperature_offset_cls = ...
    upper_deposition_limit_offset: upper_deposition_limit_offset_cls = ...
    deposition_delta_t: deposition_delta_t_cls = ...
    laplace_number_constant: laplace_number_constant_cls = ...
    partial_evaporation_ratio: partial_evaporation_ratio_cls = ...
