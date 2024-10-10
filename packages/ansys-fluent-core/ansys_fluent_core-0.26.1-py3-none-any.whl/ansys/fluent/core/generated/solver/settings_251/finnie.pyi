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

from .enabled_44 import enabled as enabled_cls
from .model_constant_k import model_constant_k as model_constant_k_cls
from .velocity_exponent import velocity_exponent as velocity_exponent_cls
from .angle_of_max_erosion import angle_of_max_erosion as angle_of_max_erosion_cls

class finnie(Group):
    fluent_name = ...
    child_names = ...
    enabled: enabled_cls = ...
    model_constant_k: model_constant_k_cls = ...
    velocity_exponent: velocity_exponent_cls = ...
    angle_of_max_erosion: angle_of_max_erosion_cls = ...
