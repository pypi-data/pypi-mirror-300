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
from .surfaces import surfaces as surfaces_cls
from .cell_func_domain_export import cell_func_domain_export as cell_func_domain_export_cls

class patran_nodal(Command):
    fluent_name = ...
    argument_names = ...
    name: name_cls = ...
    surfaces: surfaces_cls = ...
    cell_func_domain_export: cell_func_domain_export_cls = ...
    return_type = ...
