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

from .include_current_data import include_current_data as include_current_data_cls
from .objectives import objectives as objectives_cls
from .freeform_scaling_scheme import freeform_scaling_scheme as freeform_scaling_scheme_cls
from .manage_data import manage_data as manage_data_cls

class objectives(Group):
    fluent_name = ...
    child_names = ...
    include_current_data: include_current_data_cls = ...
    objectives: objectives_cls = ...
    freeform_scaling_scheme: freeform_scaling_scheme_cls = ...
    manage_data: manage_data_cls = ...
