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

from .option_3 import option as option_cls
from .none_1 import none as none_cls
from .scale_by_global_average import scale_by_global_average as scale_by_global_average_cls
from .scale_by_zone_average import scale_by_zone_average as scale_by_zone_average_cls
from .scale_by_global_maximum import scale_by_global_maximum as scale_by_global_maximum_cls
from .scale_by_zone_maximum import scale_by_zone_maximum as scale_by_zone_maximum_cls

class scaling(Group):
    fluent_name = ...
    child_names = ...
    option: option_cls = ...
    none: none_cls = ...
    scale_by_global_average: scale_by_global_average_cls = ...
    scale_by_zone_average: scale_by_zone_average_cls = ...
    scale_by_global_maximum: scale_by_global_maximum_cls = ...
    scale_by_zone_maximum: scale_by_zone_maximum_cls = ...
    return_type = ...
