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

from .name_8 import name as name_cls
from .options_12 import options as options_cls
from .edge_type import edge_type as edge_type_cls
from .shrink_factor import shrink_factor as shrink_factor_cls
from .surfaces_list import surfaces_list as surfaces_list_cls
from .coloring import coloring as coloring_cls
from .display_state_name import display_state_name as display_state_name_cls
from .physics_1 import physics as physics_cls
from .geometry_7 import geometry as geometry_cls
from .surfaces_4 import surfaces as surfaces_cls
from .display_3 import display as display_cls

class mesh_child(Group):
    fluent_name = ...
    child_names = ...
    name: name_cls = ...
    options: options_cls = ...
    edge_type: edge_type_cls = ...
    shrink_factor: shrink_factor_cls = ...
    surfaces_list: surfaces_list_cls = ...
    coloring: coloring_cls = ...
    display_state_name: display_state_name_cls = ...
    physics: physics_cls = ...
    geometry: geometry_cls = ...
    surfaces: surfaces_cls = ...
    command_names = ...

    def display(self, ):
        """
        'display' command.
        """

