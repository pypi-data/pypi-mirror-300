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

from .enabled_34 import enabled as enabled_cls
from .coolant_zone_list import coolant_zone_list as coolant_zone_list_cls
from .coolant_density import coolant_density as coolant_density_cls

class coolant_channel(Group):
    fluent_name = ...
    child_names = ...
    enabled: enabled_cls = ...
    coolant_zone_list: coolant_zone_list_cls = ...
    coolant_density: coolant_density_cls = ...
