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
from .function_of import function_of as function_of_cls
from .value_4 import value as value_cls
from .piecewise_polynomial import piecewise_polynomial as piecewise_polynomial_cls
from .piecewise_linear_1 import piecewise_linear as piecewise_linear_cls
from .polynomial_1 import polynomial as polynomial_cls

class hc(Group):
    fluent_name = ...
    child_names = ...
    option: option_cls = ...
    function_of: function_of_cls = ...
    value: value_cls = ...
    piecewise_polynomial: piecewise_polynomial_cls = ...
    piecewise_linear: piecewise_linear_cls = ...
    polynomial: polynomial_cls = ...
    return_type = ...
