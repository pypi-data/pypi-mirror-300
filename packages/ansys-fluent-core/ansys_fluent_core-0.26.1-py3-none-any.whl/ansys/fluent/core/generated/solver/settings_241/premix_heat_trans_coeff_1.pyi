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

from .option_7 import option as option_cls
from .user_defined_function import user_defined_function as user_defined_function_cls

class premix_heat_trans_coeff(Group):
    fluent_name = ...
    child_names = ...
    option: option_cls = ...
    user_defined_function: user_defined_function_cls = ...
    return_type = ...
