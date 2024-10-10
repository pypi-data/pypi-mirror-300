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

from .option_12 import option as option_cls
from .value_11 import value as value_cls
from .piecewise_linear_2 import piecewise_linear as piecewise_linear_cls
from .piecewise_polynomial import piecewise_polynomial as piecewise_polynomial_cls
from .polynomial_2 import polynomial as polynomial_cls
from .gupta_curve_fit_conductivity import gupta_curve_fit_conductivity as gupta_curve_fit_conductivity_cls
from .expression import expression as expression_cls
from .user_defined_function import user_defined_function as user_defined_function_cls
from .rgp_table import rgp_table as rgp_table_cls
from .real_gas_nist import real_gas_nist as real_gas_nist_cls

class thermal_conductivity(Group):
    """
    Thermal-conductivity property setting for this material.
    """

    fluent_name = "thermal-conductivity"

    child_names = \
        ['option', 'value', 'piecewise_linear', 'piecewise_polynomial',
         'polynomial', 'gupta_curve_fit_conductivity', 'expression',
         'user_defined_function', 'rgp_table', 'real_gas_nist']

    _child_classes = dict(
        option=option_cls,
        value=value_cls,
        piecewise_linear=piecewise_linear_cls,
        piecewise_polynomial=piecewise_polynomial_cls,
        polynomial=polynomial_cls,
        gupta_curve_fit_conductivity=gupta_curve_fit_conductivity_cls,
        expression=expression_cls,
        user_defined_function=user_defined_function_cls,
        rgp_table=rgp_table_cls,
        real_gas_nist=real_gas_nist_cls,
    )

