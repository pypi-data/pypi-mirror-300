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

from .option_12 import option as option_cls
from .value_11 import value as value_cls
from .expression import expression as expression_cls
from .polynomial_2 import polynomial as polynomial_cls
from .user_defined_function import user_defined_function as user_defined_function_cls
from .anisotropic_1 import anisotropic as anisotropic_cls
from .orthotropic import orthotropic as orthotropic_cls
from .cyl_orthotropic import cyl_orthotropic as cyl_orthotropic_cls

class uds_diffusivities_child(Group):
    fluent_name = ...
    child_names = ...
    option: option_cls = ...
    value: value_cls = ...
    expression: expression_cls = ...
    polynomial: polynomial_cls = ...
    user_defined_function: user_defined_function_cls = ...
    anisotropic: anisotropic_cls = ...
    orthotropic: orthotropic_cls = ...
    cyl_orthotropic: cyl_orthotropic_cls = ...
