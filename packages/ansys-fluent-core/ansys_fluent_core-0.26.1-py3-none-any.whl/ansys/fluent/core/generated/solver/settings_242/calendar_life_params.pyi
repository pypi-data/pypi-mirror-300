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

from .ref_temperature import ref_temperature as ref_temperature_cls
from .pre_exp_fac import pre_exp_fac as pre_exp_fac_cls
from .activation_e import activation_e as activation_e_cls
from .exponent_value import exponent_value as exponent_value_cls

class calendar_life_params(Group):
    fluent_name = ...
    child_names = ...
    ref_temperature: ref_temperature_cls = ...
    pre_exp_fac: pre_exp_fac_cls = ...
    activation_e: activation_e_cls = ...
    exponent_value: exponent_value_cls = ...
