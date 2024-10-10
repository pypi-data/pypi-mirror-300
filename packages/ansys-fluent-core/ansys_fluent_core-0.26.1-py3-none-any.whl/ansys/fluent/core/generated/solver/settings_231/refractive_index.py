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

from .option_10 import option as option_cls
from .value import value as value_cls
from .gray_band_coefficients import gray_band_coefficients as gray_band_coefficients_cls

class refractive_index(Group):
    """
    'refractive_index' child.
    """

    fluent_name = "refractive-index"

    child_names = \
        ['option', 'value', 'gray_band_coefficients']

    _child_classes = dict(
        option=option_cls,
        value=value_cls,
        gray_band_coefficients=gray_band_coefficients_cls,
    )

    return_type = "<object object at 0x7ff9d13716e0>"
