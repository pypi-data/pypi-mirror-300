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

from .mem_zone_list_1 import mem_zone_list as mem_zone_list_cls
from .mem_update import mem_update as mem_update_cls
from .mem_material import mem_material as mem_material_cls
from .mem_eqv_weight import mem_eqv_weight as mem_eqv_weight_cls
from .mem_alpha import mem_alpha as mem_alpha_cls
from .mem_beta import mem_beta as mem_beta_cls
from .mem_diff_corr import mem_diff_corr as mem_diff_corr_cls
from .mem_permeability import mem_permeability as mem_permeability_cls
from .mem_act import mem_act as mem_act_cls

class membrane(Group):
    fluent_name = ...
    child_names = ...
    mem_zone_list: mem_zone_list_cls = ...
    mem_update: mem_update_cls = ...
    mem_material: mem_material_cls = ...
    mem_eqv_weight: mem_eqv_weight_cls = ...
    mem_alpha: mem_alpha_cls = ...
    mem_beta: mem_beta_cls = ...
    mem_diff_corr: mem_diff_corr_cls = ...
    mem_permeability: mem_permeability_cls = ...
    mem_act: mem_act_cls = ...
