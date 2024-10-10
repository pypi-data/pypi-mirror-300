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

from .option import option as option_cls
from .constant import constant as constant_cls
from .coefficients import coefficients as coefficients_cls
from .number_of_coefficients import number_of_coefficients as number_of_coefficients_cls
from .piecewise_linear import piecewise_linear as piecewise_linear_cls
from .piecewise_polynomial import piecewise_polynomial as piecewise_polynomial_cls

class conductivity(Group):
    """
    'conductivity' child.
    """

    fluent_name = "conductivity"

    child_names = \
        ['option', 'constant', 'coefficients', 'number_of_coefficients',
         'piecewise_linear', 'piecewise_polynomial']

    _child_classes = dict(
        option=option_cls,
        constant=constant_cls,
        coefficients=coefficients_cls,
        number_of_coefficients=number_of_coefficients_cls,
        piecewise_linear=piecewise_linear_cls,
        piecewise_polynomial=piecewise_polynomial_cls,
    )

    return_type = "<object object at 0x7f82df9c15b0>"
