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

from .cathode_fc_zone_list import cathode_fc_zone_list as cathode_fc_zone_list_cls

class cathode_fc_zone(Group):
    fluent_name = ...
    child_names = ...
    cathode_fc_zone_list: cathode_fc_zone_list_cls = ...
    return_type = ...
