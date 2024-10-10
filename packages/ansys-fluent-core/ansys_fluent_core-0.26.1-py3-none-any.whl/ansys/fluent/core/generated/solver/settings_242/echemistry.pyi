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

from .potential import potential as potential_cls
from .joule_heating import joule_heating as joule_heating_cls
from .li_battery_enabled import li_battery_enabled as li_battery_enabled_cls
from .echemistry_enabled import echemistry_enabled as echemistry_enabled_cls
from .lithium_battery import lithium_battery as lithium_battery_cls
from .electrolysis import electrolysis as electrolysis_cls

class echemistry(Group):
    fluent_name = ...
    child_names = ...
    potential: potential_cls = ...
    joule_heating: joule_heating_cls = ...
    li_battery_enabled: li_battery_enabled_cls = ...
    echemistry_enabled: echemistry_enabled_cls = ...
    lithium_battery: lithium_battery_cls = ...
    electrolysis: electrolysis_cls = ...
