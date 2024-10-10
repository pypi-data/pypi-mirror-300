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

from .list_properties import list_properties as list_properties_cls
from .resize import resize as resize_cls
from .thin_wall_child import thin_wall_child


class thin_wall(ListObject[thin_wall_child]):
    fluent_name = ...
    command_names = ...

    def list_properties(self, object_at: int):
        """
        List properties of selected object.
        
        Parameters
        ----------
            object_at : int
                Select object index to delete.
        
        """

    def resize(self, size: int):
        """
        Set number of objects for list-object.
        
        Parameters
        ----------
            size : int
                New size for list-object.
        
        """

    child_object_type: thin_wall_child = ...
