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

from .flux_auto_select import flux_auto_select as flux_auto_select_cls
from .flux_type_1 import flux_type as flux_type_cls

class pbns_cases(Group):
    fluent_name = ...
    child_names = ...
    flux_auto_select: flux_auto_select_cls = ...
    flux_type: flux_type_cls = ...
    return_type = ...
