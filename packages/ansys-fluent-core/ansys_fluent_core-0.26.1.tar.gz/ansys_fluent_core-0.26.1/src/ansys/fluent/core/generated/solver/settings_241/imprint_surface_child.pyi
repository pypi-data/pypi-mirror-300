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
from .surface import surface as surface_cls
from .zones_4 import zones as zones_cls
from .display_3 import display as display_cls

class imprint_surface_child(Group):
    fluent_name = ...
    child_names = ...
    name: name_cls = ...
    surface: surface_cls = ...
    zones: zones_cls = ...
    command_names = ...

    def display(self, ):
        """
        'display' command.
        """

    return_type = ...
