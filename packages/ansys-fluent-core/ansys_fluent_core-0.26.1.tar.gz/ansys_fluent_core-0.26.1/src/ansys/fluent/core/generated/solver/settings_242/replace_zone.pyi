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

from .file_name_1_3 import file_name_1 as file_name_1_cls
from .zone_1_name import zone_1_name as zone_1_name_cls
from .zone_2_name import zone_2_name as zone_2_name_cls
from .interpolate import interpolate as interpolate_cls

class replace_zone(Command):
    fluent_name = ...
    argument_names = ...
    file_name: file_name_1_cls = ...
    zone_1_name: zone_1_name_cls = ...
    zone_2_name: zone_2_name_cls = ...
    interpolate: interpolate_cls = ...
