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

from .normal import normal as normal_cls
from .tangential import tangential as tangential_cls

class reflection_coefficients(Group):
    fluent_name = ...
    child_names = ...
    normal: normal_cls = ...
    tangential: tangential_cls = ...
