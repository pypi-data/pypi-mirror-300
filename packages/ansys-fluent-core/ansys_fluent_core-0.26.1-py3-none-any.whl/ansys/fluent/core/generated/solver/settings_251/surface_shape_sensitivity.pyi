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

from .method_15 import method as method_cls
from .smoothness import smoothness as smoothness_cls

class surface_shape_sensitivity(Group):
    fluent_name = ...
    child_names = ...
    method: method_cls = ...
    smoothness: smoothness_cls = ...
