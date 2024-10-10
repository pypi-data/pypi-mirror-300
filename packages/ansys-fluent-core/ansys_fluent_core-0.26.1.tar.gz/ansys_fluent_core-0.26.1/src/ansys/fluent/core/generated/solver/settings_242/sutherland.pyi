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

from .option_13 import option as option_cls
from .c1 import c1 as c1_cls
from .c2 import c2 as c2_cls
from .reference_viscosity import reference_viscosity as reference_viscosity_cls
from .reference_temperature import reference_temperature as reference_temperature_cls
from .effective_temperature import effective_temperature as effective_temperature_cls

class sutherland(Group):
    fluent_name = ...
    child_names = ...
    option: option_cls = ...
    c1: c1_cls = ...
    c2: c2_cls = ...
    reference_viscosity: reference_viscosity_cls = ...
    reference_temperature: reference_temperature_cls = ...
    effective_temperature: effective_temperature_cls = ...
