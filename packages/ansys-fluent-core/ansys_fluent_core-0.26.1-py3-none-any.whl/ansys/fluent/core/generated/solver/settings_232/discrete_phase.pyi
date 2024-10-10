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

from .general_settings import general_settings as general_settings_cls
from .injections import injections as injections_cls
from .numerics import numerics as numerics_cls
from .parallel import parallel as parallel_cls
from .physical_models_1 import physical_models as physical_models_cls
from .tracking_1 import tracking as tracking_cls
from .user_defined_functions import user_defined_functions as user_defined_functions_cls

class discrete_phase(Group):
    fluent_name = ...
    child_names = ...
    general_settings: general_settings_cls = ...
    injections: injections_cls = ...
    numerics: numerics_cls = ...
    parallel: parallel_cls = ...
    physical_models: physical_models_cls = ...
    tracking: tracking_cls = ...
    user_defined_functions: user_defined_functions_cls = ...
    return_type = ...
