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

from .option import option as option_cls
from .consistency_index import consistency_index as consistency_index_cls
from .power_law_index import power_law_index as power_law_index_cls
from .yield_stress_threshold import yield_stress_threshold as yield_stress_threshold_cls
from .critical_shear_rate import critical_shear_rate as critical_shear_rate_cls
from .reference_temperature import reference_temperature as reference_temperature_cls
from .activation_energy import activation_energy as activation_energy_cls

class herschel_bulkley(Group):
    fluent_name = ...
    child_names = ...
    option: option_cls = ...
    consistency_index: consistency_index_cls = ...
    power_law_index: power_law_index_cls = ...
    yield_stress_threshold: yield_stress_threshold_cls = ...
    critical_shear_rate: critical_shear_rate_cls = ...
    reference_temperature: reference_temperature_cls = ...
    activation_energy: activation_energy_cls = ...
    return_type = ...
