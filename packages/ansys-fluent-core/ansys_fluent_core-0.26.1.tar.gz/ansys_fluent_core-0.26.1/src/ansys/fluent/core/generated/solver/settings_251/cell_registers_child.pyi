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

from .name_14 import name as name_cls
from .python_name_1 import python_name_1 as python_name_1_cls
from .type_8 import type as type_cls
from .display_options import display_options as display_options_cls
from .create_volume_surface import create_volume_surface as create_volume_surface_cls

class cell_registers_child(Group):
    fluent_name = ...
    child_names = ...
    name: name_cls = ...
    python_name_1: python_name_1_cls = ...
    type: type_cls = ...
    display_options: display_options_cls = ...
    command_names = ...

    def create_volume_surface(self, ):
        """
        Create a volume surface.
        """

