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

from .option_10 import option as option_cls
from .user_defined_function import user_defined_function as user_defined_function_cls
from .value import value as value_cls
from .piecewise_linear import piecewise_linear as piecewise_linear_cls
from .piecewise_polynomial import piecewise_polynomial as piecewise_polynomial_cls
from .polynomial import polynomial as polynomial_cls
from .nasa_9_piecewise_polynomial import nasa_9_piecewise_polynomial as nasa_9_piecewise_polynomial_cls

class specific_heat(Group):
    fluent_name = ...
    child_names = ...
    option: option_cls = ...
    user_defined_function: user_defined_function_cls = ...
    value: value_cls = ...
    piecewise_linear: piecewise_linear_cls = ...
    piecewise_polynomial: piecewise_polynomial_cls = ...
    polynomial: polynomial_cls = ...
    nasa_9_piecewise_polynomial: nasa_9_piecewise_polynomial_cls = ...
    return_type = ...
