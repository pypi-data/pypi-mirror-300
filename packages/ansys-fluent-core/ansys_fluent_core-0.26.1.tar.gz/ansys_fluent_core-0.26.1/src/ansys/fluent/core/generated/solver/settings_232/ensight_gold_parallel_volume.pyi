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

from .name import name as name_cls
from .binary_format import binary_format as binary_format_cls
from .cellzones import cellzones as cellzones_cls
from .cell_centered import cell_centered as cell_centered_cls
from .cell_function import cell_function as cell_function_cls

class ensight_gold_parallel_volume(Command):
    fluent_name = ...
    argument_names = ...
    name: name_cls = ...
    binary_format: binary_format_cls = ...
    cellzones: cellzones_cls = ...
    cell_centered: cell_centered_cls = ...
    cell_function: cell_function_cls = ...
    return_type = ...
