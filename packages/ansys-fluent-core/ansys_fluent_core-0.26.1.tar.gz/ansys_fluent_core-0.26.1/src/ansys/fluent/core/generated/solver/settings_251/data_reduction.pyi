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

from .across_injections_enabled import across_injections_enabled as across_injections_enabled_cls
from .min_parcel_count import min_parcel_count as min_parcel_count_cls

class data_reduction(Group):
    fluent_name = ...
    child_names = ...
    across_injections_enabled: across_injections_enabled_cls = ...
    min_parcel_count: min_parcel_count_cls = ...
