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

from .init_from_data_file import init_from_data_file as init_from_data_file_cls
from .init_from_solution import init_from_solution as init_from_solution_cls

class initialization_method(Group):
    fluent_name = ...
    child_names = ...
    init_from_data_file: init_from_data_file_cls = ...
    init_from_solution: init_from_solution_cls = ...
