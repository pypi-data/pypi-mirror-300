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

from .enabled_15 import enabled as enabled_cls
from .set_2 import set as set_cls

class laplace_smoothing(Group):
    fluent_name = ...
    child_names = ...
    enabled: enabled_cls = ...
    set: set_cls = ...
    return_type = ...
