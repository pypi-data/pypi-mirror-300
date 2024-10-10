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

from .enable_5 import enable as enable_cls
from .robustness_enhancement import robustness_enhancement as robustness_enhancement_cls
from .nasa9_enhancement import nasa9_enhancement as nasa9_enhancement_cls
from .set_verbosity import set_verbosity as set_verbosity_cls
from .translational_vibrational_energy_relaxation import translational_vibrational_energy_relaxation as translational_vibrational_energy_relaxation_cls

class two_temperature(Group):
    fluent_name = ...
    child_names = ...
    enable: enable_cls = ...
    robustness_enhancement: robustness_enhancement_cls = ...
    nasa9_enhancement: nasa9_enhancement_cls = ...
    set_verbosity: set_verbosity_cls = ...
    translational_vibrational_energy_relaxation: translational_vibrational_energy_relaxation_cls = ...
    return_type = ...
