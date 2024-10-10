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
from .user_defined_function import user_defined_function as user_defined_function_cls

class premix_adiabatic_temp(Group):
    """
    Premix-adiabatic-temp property setting for this material.
    """

    fluent_name = "premix-adiabatic-temp"

    child_names = \
        ['option', 'value', 'user_defined_function']

    _child_classes = dict(
        option=option_cls,
        value=value_cls,
        user_defined_function=user_defined_function_cls,
    )

