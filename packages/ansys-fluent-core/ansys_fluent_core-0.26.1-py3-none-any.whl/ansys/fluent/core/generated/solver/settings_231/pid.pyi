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

from .method_1 import method as method_cls
from .number_of_coeff import number_of_coeff as number_of_coeff_cls
from .function_of import function_of as function_of_cls
from .coefficients_1 import coefficients as coefficients_cls
from .constant import constant as constant_cls
from .piecewise_polynomial_1 import piecewise_polynomial as piecewise_polynomial_cls
from .piecewise_linear import piecewise_linear as piecewise_linear_cls

class pid(Group):
    fluent_name = ...
    child_names = ...
    method: method_cls = ...
    number_of_coeff: number_of_coeff_cls = ...
    function_of: function_of_cls = ...
    coefficients: coefficients_cls = ...
    constant: constant_cls = ...
    piecewise_polynomial: piecewise_polynomial_cls = ...
    piecewise_linear: piecewise_linear_cls = ...
    return_type = ...
