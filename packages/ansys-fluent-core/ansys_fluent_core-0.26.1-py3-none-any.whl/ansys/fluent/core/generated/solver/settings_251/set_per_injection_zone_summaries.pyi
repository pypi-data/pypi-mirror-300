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

from .enable_25 import enable as enable_cls
from .reset_dpm_summaries import reset_dpm_summaries as reset_dpm_summaries_cls

class set_per_injection_zone_summaries(Command):
    fluent_name = ...
    argument_names = ...
    enable: enable_cls = ...
    reset_dpm_summaries: reset_dpm_summaries_cls = ...
