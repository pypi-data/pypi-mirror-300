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

from .numbers import numbers as numbers_cls
from .rules import rules as rules_cls
from .log_scale_2 import log_scale as log_scale_cls
from .auto_scale_1 import auto_scale as auto_scale_cls
from .labels import labels as labels_cls

class axes(Group):
    fluent_name = ...
    child_names = ...
    numbers: numbers_cls = ...
    rules: rules_cls = ...
    log_scale: log_scale_cls = ...
    auto_scale: auto_scale_cls = ...
    labels: labels_cls = ...
    return_type = ...
