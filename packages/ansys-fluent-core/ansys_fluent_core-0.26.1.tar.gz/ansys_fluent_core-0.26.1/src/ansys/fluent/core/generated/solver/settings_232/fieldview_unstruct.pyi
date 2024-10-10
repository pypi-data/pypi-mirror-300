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
from .surfaces_1 import surfaces as surfaces_cls
from .cellzones_1 import cellzones as cellzones_cls
from .cell_func_domain import cell_func_domain as cell_func_domain_cls

class fieldview_unstruct(Command):
    fluent_name = ...
    argument_names = ...
    name: name_cls = ...
    surfaces: surfaces_cls = ...
    cellzones: cellzones_cls = ...
    cell_func_domain: cell_func_domain_cls = ...
    return_type = ...
