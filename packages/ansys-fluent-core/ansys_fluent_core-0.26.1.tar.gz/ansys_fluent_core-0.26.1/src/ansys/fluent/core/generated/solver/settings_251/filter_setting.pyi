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

from .enabled_66 import enabled as enabled_cls
from .field_9 import field as field_cls
from .option_48 import option as option_cls
from .range_4 import range as range_cls

class filter_setting(Group):
    fluent_name = ...
    child_names = ...
    enabled: enabled_cls = ...
    field: field_cls = ...
    option: option_cls = ...
    range: range_cls = ...
