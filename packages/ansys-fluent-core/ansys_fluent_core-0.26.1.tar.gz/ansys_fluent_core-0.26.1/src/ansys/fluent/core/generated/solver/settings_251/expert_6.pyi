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

from .mass_flux_correction_method import mass_flux_correction_method as mass_flux_correction_method_cls
from .hybrid_mode_selection import hybrid_mode_selection as hybrid_mode_selection_cls

class expert(Group):
    fluent_name = ...
    child_names = ...
    mass_flux_correction_method: mass_flux_correction_method_cls = ...
    hybrid_mode_selection: hybrid_mode_selection_cls = ...
