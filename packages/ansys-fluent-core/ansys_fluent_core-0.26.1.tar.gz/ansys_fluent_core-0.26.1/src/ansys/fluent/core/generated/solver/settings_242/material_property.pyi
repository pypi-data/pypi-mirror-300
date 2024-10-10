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

from .cathode_cmax import cathode_cmax as cathode_cmax_cls
from .anode_cmax import anode_cmax as anode_cmax_cls
from .cathode_c_init import cathode_c_init as cathode_c_init_cls
from .anode_c_init import anode_c_init as anode_c_init_cls
from .electrolyte_c_init import electrolyte_c_init as electrolyte_c_init_cls
from .tplus import tplus as tplus_cls
from .activity_term import activity_term as activity_term_cls

class material_property(Group):
    fluent_name = ...
    child_names = ...
    cathode_cmax: cathode_cmax_cls = ...
    anode_cmax: anode_cmax_cls = ...
    cathode_c_init: cathode_c_init_cls = ...
    anode_c_init: anode_c_init_cls = ...
    electrolyte_c_init: electrolyte_c_init_cls = ...
    tplus: tplus_cls = ...
    activity_term: activity_term_cls = ...
