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

from .format_type import format_type as format_type_cls
from .precision import precision as precision_cls

class number_format(Group):
    fluent_name = ...
    child_names = ...
    format_type: format_type_cls = ...
    precision: precision_cls = ...
    return_type = ...
