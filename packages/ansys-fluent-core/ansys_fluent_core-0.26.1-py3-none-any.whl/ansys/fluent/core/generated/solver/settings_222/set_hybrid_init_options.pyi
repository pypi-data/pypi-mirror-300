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
from .turbulent_setting import turbulent_setting as turbulent_setting_cls

class set_hybrid_init_options(Group):
    fluent_name = ...
    child_names = ...
    general_settings: general_settings_cls = ...
    turbulent_setting: turbulent_setting_cls = ...
    return_type = ...
