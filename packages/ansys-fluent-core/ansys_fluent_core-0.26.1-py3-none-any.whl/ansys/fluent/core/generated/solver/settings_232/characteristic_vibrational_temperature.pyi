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

from .option_10 import option as option_cls
from .vibrational_modes import vibrational_modes as vibrational_modes_cls
from .value_1 import value as value_cls

class characteristic_vibrational_temperature(Group):
    fluent_name = ...
    child_names = ...
    option: option_cls = ...
    vibrational_modes: vibrational_modes_cls = ...
    value: value_cls = ...
    return_type = ...
