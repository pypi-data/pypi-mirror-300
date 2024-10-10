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

from .direction_0 import direction_0 as direction_0_cls
from .direction_1 import direction_1 as direction_1_cls
from .diffusivity_0 import diffusivity_0 as diffusivity_0_cls
from .diffusivity_1 import diffusivity_1 as diffusivity_1_cls
from .diffusivity_2 import diffusivity_2 as diffusivity_2_cls

class orthotropic(Group):
    fluent_name = ...
    child_names = ...
    direction_0: direction_0_cls = ...
    direction_1: direction_1_cls = ...
    diffusivity_0: diffusivity_0_cls = ...
    diffusivity_1: diffusivity_1_cls = ...
    diffusivity_2: diffusivity_2_cls = ...
    return_type = ...
