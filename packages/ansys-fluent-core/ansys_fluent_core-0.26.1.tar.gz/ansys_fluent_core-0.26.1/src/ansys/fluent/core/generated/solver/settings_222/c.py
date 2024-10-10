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

from .method import method as method_cls
from .number_of_coeff import number_of_coeff as number_of_coeff_cls
from .function_of import function_of as function_of_cls
from .coefficients import coefficients as coefficients_cls
from .constant import constant as constant_cls
from .piecewise_polynomial import piecewise_polynomial as piecewise_polynomial_cls
from .piecewise_linear import piecewise_linear as piecewise_linear_cls

class c(Group):
    """
    'c' child.
    """

    fluent_name = "c"

    child_names = \
        ['method', 'number_of_coeff', 'function_of', 'coefficients',
         'constant', 'piecewise_polynomial', 'piecewise_linear']

    _child_classes = dict(
        method=method_cls,
        number_of_coeff=number_of_coeff_cls,
        function_of=function_of_cls,
        coefficients=coefficients_cls,
        constant=constant_cls,
        piecewise_polynomial=piecewise_polynomial_cls,
        piecewise_linear=piecewise_linear_cls,
    )

    return_type = "<object object at 0x7f82c68c1920>"
