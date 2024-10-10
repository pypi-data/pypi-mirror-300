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

from .name_2 import name as name_cls
from .location_2 import location as location_cls
from .settings_12 import settings as settings_cls
from .split import split as split_cls

class mass_flow_inlet_child(Group):
    fluent_name = ...
    child_names = ...
    name: name_cls = ...
    location: location_cls = ...
    settings: settings_cls = ...
    command_names = ...

    def split(self, name: str, location: List[str]):
        """
        Input boundary and location names to split.
        
        Parameters
        ----------
            name : str
                Input new boundary name.
            location : List
                Input location name which should be part of new boundary.
        
        """

