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

from .echem_stop_type import echem_stop_type as echem_stop_type_cls
from .min_voltage import min_voltage as min_voltage_cls
from .max_voltage import max_voltage as max_voltage_cls
from .min_soc import min_soc as min_soc_cls
from .max_soc import max_soc as max_soc_cls

class echem_stop_criterion(Group):
    fluent_name = ...
    child_names = ...
    echem_stop_type: echem_stop_type_cls = ...
    min_voltage: min_voltage_cls = ...
    max_voltage: max_voltage_cls = ...
    min_soc: min_soc_cls = ...
    max_soc: max_soc_cls = ...
