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

from .formulation import formulation as formulation_cls
from .local_time_step_settings import local_time_step_settings as local_time_step_settings_cls
from .global_time_step_settings import global_time_step_settings as global_time_step_settings_cls
from .advanced_options import advanced_options as advanced_options_cls
from .relaxation_factors import relaxation_factors as relaxation_factors_cls
from .verbosity_3 import verbosity as verbosity_cls

class pseudo_time_method(Group):
    fluent_name = ...
    child_names = ...
    formulation: formulation_cls = ...
    local_time_step_settings: local_time_step_settings_cls = ...
    global_time_step_settings: global_time_step_settings_cls = ...
    advanced_options: advanced_options_cls = ...
    relaxation_factors: relaxation_factors_cls = ...
    verbosity: verbosity_cls = ...
    return_type = ...
