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

from .min_value import min_value as min_value_cls
from .max_value import max_value as max_value_cls

class clip_to_range(Group):
    fluent_name = ...
    child_names = ...
    min_value: min_value_cls = ...
    max_value: max_value_cls = ...
    return_type = ...
