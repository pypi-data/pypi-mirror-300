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

from .cathode_cl_zone_list import cathode_cl_zone_list as cathode_cl_zone_list_cls
from .cathode_cl_update import cathode_cl_update as cathode_cl_update_cls
from .cathode_cl_material import cathode_cl_material as cathode_cl_material_cls
from .cathode_cl_porosity import cathode_cl_porosity as cathode_cl_porosity_cls
from .cathode_cl_kr import cathode_cl_kr as cathode_cl_kr_cls

class cathode_cl_zone(Group):
    fluent_name = ...
    child_names = ...
    cathode_cl_zone_list: cathode_cl_zone_list_cls = ...
    cathode_cl_update: cathode_cl_update_cls = ...
    cathode_cl_material: cathode_cl_material_cls = ...
    cathode_cl_porosity: cathode_cl_porosity_cls = ...
    cathode_cl_kr: cathode_cl_kr_cls = ...
    return_type = ...
