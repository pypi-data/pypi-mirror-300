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

from .temperature_1 import temperature as temperature_cls
from .vibrational_electronic_temperature import vibrational_electronic_temperature as vibrational_electronic_temperature_cls

class thermal(Group):
    fluent_name = ...
    child_names = ...
    temperature: temperature_cls = ...
    vibrational_electronic_temperature: vibrational_electronic_temperature_cls = ...
