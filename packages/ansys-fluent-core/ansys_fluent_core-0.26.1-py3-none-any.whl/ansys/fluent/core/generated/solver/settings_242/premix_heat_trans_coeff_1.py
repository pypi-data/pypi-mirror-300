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
from .user_defined_function import user_defined_function as user_defined_function_cls

class premix_heat_trans_coeff(Group):
    """
    Premix-heat-trans-coeff property setting for this material.
    """

    fluent_name = "premix-heat-trans-coeff"

    child_names = \
        ['option', 'user_defined_function']

    _child_classes = dict(
        option=option_cls,
        user_defined_function=user_defined_function_cls,
    )

