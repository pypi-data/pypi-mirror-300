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

from .voltage_tap import voltage_tap as voltage_tap_cls
from .current_tap import current_tap as current_tap_cls
from .conductive_regions import conductive_regions as conductive_regions_cls
from .contact_resistance_regions import contact_resistance_regions as contact_resistance_regions_cls

class electric_field(Group):
    fluent_name = ...
    child_names = ...
    voltage_tap: voltage_tap_cls = ...
    current_tap: current_tap_cls = ...
    conductive_regions: conductive_regions_cls = ...
    contact_resistance_regions: contact_resistance_regions_cls = ...
