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

from .thermal_bc import thermal_bc as thermal_bc_cls
from .temperature_1 import temperature as temperature_cls
from .q import q as q_cls

class network_end(Group):
    fluent_name = ...
    child_names = ...
    thermal_bc: thermal_bc_cls = ...
    temperature: temperature_cls = ...
    q: q_cls = ...
