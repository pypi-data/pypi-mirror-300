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

from .method_16 import method as method_cls
from .constraint_method import constraint_method as constraint_method_cls
from .numerics_1 import numerics as numerics_cls

class morpher(Group):
    fluent_name = ...
    child_names = ...
    method: method_cls = ...
    constraint_method: constraint_method_cls = ...
    numerics: numerics_cls = ...
