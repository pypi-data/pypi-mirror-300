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

from .differential_viscosity_model import differential_viscosity_model as differential_viscosity_model_cls
from .swirl_dominated_flow import swirl_dominated_flow as swirl_dominated_flow_cls

class rng_options(Group):
    fluent_name = ...
    child_names = ...
    differential_viscosity_model: differential_viscosity_model_cls = ...
    swirl_dominated_flow: swirl_dominated_flow_cls = ...
    return_type = ...
