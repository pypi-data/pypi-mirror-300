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

from .option import option as option_cls
from .step_size import step_size as step_size_cls
from .tolerance_2 import tolerance as tolerance_cls

class accuracy_control(Group):
    fluent_name = ...
    child_names = ...
    option: option_cls = ...
    step_size: step_size_cls = ...
    tolerance: tolerance_cls = ...
    return_type = ...
