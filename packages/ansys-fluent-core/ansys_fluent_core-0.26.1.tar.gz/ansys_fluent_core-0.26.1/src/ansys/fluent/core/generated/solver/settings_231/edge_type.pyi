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

from .option_3 import option as option_cls
from .all import all as all_cls
from .feature import feature as feature_cls
from .outline import outline as outline_cls

class edge_type(Group):
    fluent_name = ...
    child_names = ...
    option: option_cls = ...
    all: all_cls = ...
    feature: feature_cls = ...
    outline: outline_cls = ...
    return_type = ...
