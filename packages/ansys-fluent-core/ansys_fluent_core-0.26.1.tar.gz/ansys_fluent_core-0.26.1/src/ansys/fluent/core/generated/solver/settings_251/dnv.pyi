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

from .enabled_47 import enabled as enabled_cls
from .model_constant_k import model_constant_k as model_constant_k_cls
from .model_constant_n import model_constant_n as model_constant_n_cls
from .ductile_material_enabled import ductile_material_enabled as ductile_material_enabled_cls

class dnv(Group):
    fluent_name = ...
    child_names = ...
    enabled: enabled_cls = ...
    model_constant_k: model_constant_k_cls = ...
    model_constant_n: model_constant_n_cls = ...
    ductile_material_enabled: ductile_material_enabled_cls = ...
