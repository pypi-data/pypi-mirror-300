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

from .change_type import change_type as change_type_cls
from .recirculation_outlet_child import recirculation_outlet_child


class recirculation_outlet(NamedObject[recirculation_outlet_child], CreatableNamedObjectMixinOld[recirculation_outlet_child]):
    fluent_name = ...
    command_names = ...

    def change_type(self, zone_list: List[str], new_type: str):
        """
        'change_type' command.
        
        Parameters
        ----------
            zone_list : List
                'zone_list' child.
            new_type : str
                'new_type' child.
        
        """

    child_object_type: recirculation_outlet_child = ...
    return_type = ...
