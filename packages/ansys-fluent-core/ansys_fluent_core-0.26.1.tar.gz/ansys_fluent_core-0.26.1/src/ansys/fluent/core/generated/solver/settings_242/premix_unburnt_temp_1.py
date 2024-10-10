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

class premix_unburnt_temp(Group):
    """
    Premix-unburnt-temp property setting for this material.
    """

    fluent_name = "premix-unburnt-temp"

    child_names = \
        ['option', 'user_defined_function']

    _child_classes = dict(
        option=option_cls,
        user_defined_function=user_defined_function_cls,
    )

