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

from .observable_2 import observable as observable_cls
from .value_17 import value as value_cls
from .step_direction import step_direction as step_direction_cls
from .target_change import target_change as target_change_cls
from .change_as_percentage import change_as_percentage as change_as_percentage_cls
from .weight_3 import weight as weight_cls

class objectives_child(Group):
    fluent_name = ...
    child_names = ...
    observable: observable_cls = ...
    value: value_cls = ...
    step_direction: step_direction_cls = ...
    target_change: target_change_cls = ...
    change_as_percentage: change_as_percentage_cls = ...
    weight: weight_cls = ...
