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

from .option_8 import option as option_cls
from .virtual_mass_factor import virtual_mass_factor as virtual_mass_factor_cls

class virtual_mass_force(Group):
    fluent_name = ...
    child_names = ...
    option: option_cls = ...
    virtual_mass_factor: virtual_mass_factor_cls = ...
    return_type = ...
