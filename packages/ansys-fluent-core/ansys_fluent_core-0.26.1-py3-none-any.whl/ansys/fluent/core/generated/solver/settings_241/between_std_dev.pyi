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

from .lower import lower as lower_cls
from .upper import upper as upper_cls

class between_std_dev(Group):
    fluent_name = ...
    child_names = ...
    lower: lower_cls = ...
    upper: upper_cls = ...
    return_type = ...
