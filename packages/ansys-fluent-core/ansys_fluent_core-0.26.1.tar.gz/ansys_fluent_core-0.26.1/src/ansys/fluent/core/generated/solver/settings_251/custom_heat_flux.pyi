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
from .wall_function import wall_function as wall_function_cls
from .surface_name_list_2 import surface_name_list as surface_name_list_cls

class custom_heat_flux(Command):
    fluent_name = ...
    argument_names = ...
    file_name: file_name_cls = ...
    wall_function: wall_function_cls = ...
    surface_name_list: surface_name_list_cls = ...
