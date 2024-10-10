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

from .domain import domain as domain_cls
from .cell_function_1 import cell_function as cell_function_cls
from .min_val import min_val as min_val_cls
from .max_val import max_val as max_val_cls
from .num_division import num_division as num_division_cls
from .set_all_zones import set_all_zones as set_all_zones_cls
from .threads_list import threads_list as threads_list_cls
from .file_name_1 import file_name as file_name_cls
from .overwrite import overwrite as overwrite_cls

class write(Command):
    fluent_name = ...
    argument_names = ...
    domain: domain_cls = ...
    cell_function: cell_function_cls = ...
    min_val: min_val_cls = ...
    max_val: max_val_cls = ...
    num_division: num_division_cls = ...
    set_all_zones: set_all_zones_cls = ...
    threads_list: threads_list_cls = ...
    file_name: file_name_cls = ...
    overwrite: overwrite_cls = ...
    return_type = ...
