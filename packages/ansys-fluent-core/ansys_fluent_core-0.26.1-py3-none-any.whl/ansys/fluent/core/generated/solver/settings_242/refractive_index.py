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
from .gray_band_coefficients import gray_band_coefficients as gray_band_coefficients_cls

class refractive_index(Group):
    """
    Refractive-index property setting for this material.
    """

    fluent_name = "refractive-index"

    child_names = \
        ['option', 'value', 'gray_band_coefficients']

    _child_classes = dict(
        option=option_cls,
        value=value_cls,
        gray_band_coefficients=gray_band_coefficients_cls,
    )

