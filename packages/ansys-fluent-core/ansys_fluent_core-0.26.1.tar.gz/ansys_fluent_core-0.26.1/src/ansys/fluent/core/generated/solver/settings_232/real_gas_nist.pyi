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

from .nist_fluid import nist_fluid as nist_fluid_cls
from .lookup_table import lookup_table as lookup_table_cls
from .pressure_points import pressure_points as pressure_points_cls
from .pressure_minimum import pressure_minimum as pressure_minimum_cls
from .pressure_maximum import pressure_maximum as pressure_maximum_cls
from .temperature_points import temperature_points as temperature_points_cls
from .temperature_minimum import temperature_minimum as temperature_minimum_cls
from .temperature_maximum import temperature_maximum as temperature_maximum_cls
from .saturation_points import saturation_points as saturation_points_cls

class real_gas_nist(Group):
    fluent_name = ...
    child_names = ...
    nist_fluid: nist_fluid_cls = ...
    lookup_table: lookup_table_cls = ...
    pressure_points: pressure_points_cls = ...
    pressure_minimum: pressure_minimum_cls = ...
    pressure_maximum: pressure_maximum_cls = ...
    temperature_points: temperature_points_cls = ...
    temperature_minimum: temperature_minimum_cls = ...
    temperature_maximum: temperature_maximum_cls = ...
    saturation_points: saturation_points_cls = ...
    return_type = ...
