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

from .enabled_13 import enabled as enabled_cls
from .ddpm_phase import ddpm_phase as ddpm_phase_cls

class volume_displacement(Group):
    fluent_name = ...
    child_names = ...
    enabled: enabled_cls = ...
    ddpm_phase: ddpm_phase_cls = ...
