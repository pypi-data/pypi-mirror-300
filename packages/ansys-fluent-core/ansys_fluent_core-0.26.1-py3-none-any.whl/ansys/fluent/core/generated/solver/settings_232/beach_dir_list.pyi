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

from .list_properties_1 import list_properties as list_properties_cls
from .beach_dir_list_child import beach_dir_list_child


class beach_dir_list(ListObject[beach_dir_list_child]):
    fluent_name = ...
    command_names = ...

    def list_properties(self, object_at: int):
        """
        'list_properties' command.
        
        Parameters
        ----------
            object_at : int
                'object_at' child.
        
        """

    child_object_type: beach_dir_list_child = ...
    return_type = ...
