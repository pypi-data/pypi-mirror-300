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
from .user_defined_function import user_defined_function as user_defined_function_cls

class vp_equilib(Group):
    """
    'vp_equilib' child.
    """

    fluent_name = "vp-equilib"

    child_names = \
        ['option', 'user_defined_function']

    _child_classes = dict(
        option=option_cls,
        user_defined_function=user_defined_function_cls,
    )

    return_type = "<object object at 0x7ff9d1a03800>"
