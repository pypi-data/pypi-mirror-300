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

from .eload_settings import eload_settings as eload_settings_cls
from .echem_stop_criterion import echem_stop_criterion as echem_stop_criterion_cls

class eload_condition(Group):
    fluent_name = ...
    child_names = ...
    eload_settings: eload_settings_cls = ...
    echem_stop_criterion: echem_stop_criterion_cls = ...
