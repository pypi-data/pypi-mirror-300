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
from .surfaces_2 import surfaces as surfaces_cls
from .cell_func_domain_export import cell_func_domain_export as cell_func_domain_export_cls

class patran_nodal(Command):
    fluent_name = ...
    argument_names = ...
    file_name: file_name_cls = ...
    surfaces: surfaces_cls = ...
    cell_func_domain_export: cell_func_domain_export_cls = ...
