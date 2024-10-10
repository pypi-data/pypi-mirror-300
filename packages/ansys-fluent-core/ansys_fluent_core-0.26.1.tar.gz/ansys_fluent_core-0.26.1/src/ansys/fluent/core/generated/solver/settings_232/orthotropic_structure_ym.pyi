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
from .youngs_modulus_0 import youngs_modulus_0 as youngs_modulus_0_cls
from .youngs_modulus_1 import youngs_modulus_1 as youngs_modulus_1_cls
from .youngs_modulus_2 import youngs_modulus_2 as youngs_modulus_2_cls
from .shear_modulus_01 import shear_modulus_01 as shear_modulus_01_cls
from .shear_modulus_12 import shear_modulus_12 as shear_modulus_12_cls
from .shear_modulus_02 import shear_modulus_02 as shear_modulus_02_cls

class orthotropic_structure_ym(Group):
    fluent_name = ...
    child_names = ...
    direction_0: direction_0_cls = ...
    direction_1: direction_1_cls = ...
    youngs_modulus_0: youngs_modulus_0_cls = ...
    youngs_modulus_1: youngs_modulus_1_cls = ...
    youngs_modulus_2: youngs_modulus_2_cls = ...
    shear_modulus_01: shear_modulus_01_cls = ...
    shear_modulus_12: shear_modulus_12_cls = ...
    shear_modulus_02: shear_modulus_02_cls = ...
    return_type = ...
