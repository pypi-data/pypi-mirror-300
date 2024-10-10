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

from .option_12 import option as option_cls
from .value_11 import value as value_cls
from .piecewise_linear_2 import piecewise_linear as piecewise_linear_cls
from .piecewise_polynomial import piecewise_polynomial as piecewise_polynomial_cls
from .polynomial_2 import polynomial as polynomial_cls
from .user_defined_function import user_defined_function as user_defined_function_cls

class dual_electric_conductivity(Group):
    fluent_name = ...
    child_names = ...
    option: option_cls = ...
    value: value_cls = ...
    piecewise_linear: piecewise_linear_cls = ...
    piecewise_polynomial: piecewise_polynomial_cls = ...
    polynomial: polynomial_cls = ...
    user_defined_function: user_defined_function_cls = ...
