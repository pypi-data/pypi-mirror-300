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

from .file_name_1 import file_name as file_name_cls
from .scope import scope as scope_cls
from .cell_zones import cell_zones as cell_zones_cls
from .surfaces import surfaces as surfaces_cls
from .cell_centered import cell_centered as cell_centered_cls
from .format_class import format_class as format_class_cls
from .cgns_scalar import cgns_scalar as cgns_scalar_cls

class cgns(Command):
    fluent_name = ...
    argument_names = ...
    file_name: file_name_cls = ...
    scope: scope_cls = ...
    cell_zones: cell_zones_cls = ...
    surfaces: surfaces_cls = ...
    cell_centered: cell_centered_cls = ...
    format_class: format_class_cls = ...
    cgns_scalar: cgns_scalar_cls = ...
