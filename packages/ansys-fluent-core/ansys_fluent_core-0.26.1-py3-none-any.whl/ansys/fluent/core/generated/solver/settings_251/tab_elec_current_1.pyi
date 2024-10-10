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

from .option_25 import option as option_cls
from .value_13 import value as value_cls
from .profile_4 import profile as profile_cls

class tab_elec_current(Group):
    fluent_name = ...
    child_names = ...
    option: option_cls = ...
    value: value_cls = ...
    profile: profile_cls = ...
