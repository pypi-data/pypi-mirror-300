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

from .solar_frequency_data import solar_frequency_data as solar_frequency_data_cls
from .solar_filename import solar_filename as solar_filename_cls

class autoread_solar_data(Group):
    fluent_name = ...
    child_names = ...
    solar_frequency_data: solar_frequency_data_cls = ...
    solar_filename: solar_filename_cls = ...
    return_type = ...
