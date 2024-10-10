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

from .option_7 import option as option_cls
from .value_3 import value as value_cls
from .single_rate import single_rate as single_rate_cls
from .two_competing_rates import two_competing_rates as two_competing_rates_cls
from .cpd_model import cpd_model as cpd_model_cls

class devolatilization_model(Group):
    fluent_name = ...
    child_names = ...
    option: option_cls = ...
    value: value_cls = ...
    single_rate: single_rate_cls = ...
    two_competing_rates: two_competing_rates_cls = ...
    cpd_model: cpd_model_cls = ...
    return_type = ...
