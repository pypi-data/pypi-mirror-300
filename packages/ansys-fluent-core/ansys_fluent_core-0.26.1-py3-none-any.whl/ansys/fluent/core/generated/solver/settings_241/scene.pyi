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

from .delete_1 import delete as delete_cls
from .list import list as list_cls
from .list_properties_1 import list_properties as list_properties_cls
from .make_a_copy import make_a_copy as make_a_copy_cls
from .display_2 import display as display_cls
from .copy_4 import copy as copy_cls
from .add_to_graphics import add_to_graphics as add_to_graphics_cls
from .clear_history import clear_history as clear_history_cls
from .scene_child import scene_child


class scene(NamedObject[scene_child], CreatableNamedObjectMixinOld[scene_child]):
    fluent_name = ...
    command_names = ...

    def delete(self, name_list: List[str]):
        """
        Delete selected objects.
        
        Parameters
        ----------
            name_list : List
                Select objects to be deleted.
        
        """

    def list(self, ):
        """
        List the names of the objects.
        """

    def list_properties(self, object_name: str):
        """
        List active properties of the object.
        
        Parameters
        ----------
            object_name : str
                Select object for which properties are to be listed.
        
        """

    def make_a_copy(self, from_: str, to: str):
        """
        Create a copy of the object.
        
        Parameters
        ----------
            from_ : str
                Select the object to duplicate.
            to : str
                Specify the name of the new object.
        
        """

    def display(self, object_name: str):
        """
        Display graphics object.
        
        Parameters
        ----------
            object_name : str
                'object_name' child.
        
        """

    def copy(self, from_name: str, new_name: str):
        """
        Copy graphics object.
        
        Parameters
        ----------
            from_name : str
                'from_name' child.
            new_name : str
                'new_name' child.
        
        """

    def add_to_graphics(self, object_name: str):
        """
        Add graphics object to existing graphics.
        
        Parameters
        ----------
            object_name : str
                'object_name' child.
        
        """

    def clear_history(self, object_name: str):
        """
        Clear object history.
        
        Parameters
        ----------
            object_name : str
                'object_name' child.
        
        """

    child_object_type: scene_child = ...
    return_type = ...
