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

from .option import option as option_cls
from .shape_factor import shape_factor as shape_factor_cls
from .cunningham_factor import cunningham_factor as cunningham_factor_cls

class particle_drag(Group):
    fluent_name = ...
    child_names = ...
    option: option_cls = ...
    shape_factor: shape_factor_cls = ...
    cunningham_factor: cunningham_factor_cls = ...
    return_type = ...
