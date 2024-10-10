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
from .rename import rename as rename_cls
from .list_3 import list as list_cls
from .list_properties_1 import list_properties as list_properties_cls
from .make_a_copy import make_a_copy as make_a_copy_cls
from .use_active import use_active as use_active_cls
from .restore_state import restore_state as restore_state_cls
from .copy_5 import copy as copy_cls
from .read_3 import read as read_cls
from .write_1 import write as write_cls
from .display_states_child import display_states_child


class display_states(NamedObject[display_states_child], CreatableNamedObjectMixinOld[display_states_child]):
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

    def rename(self, new: str, old: str):
        """
        Rename the object.
        
        Parameters
        ----------
            new : str
                New name for the object.
            old : str
                Select object to rename.
        
        """

    def list(self, ):
        """
        'list' command.
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

    def use_active(self, state_name: str):
        """
        'use_active' command.
        
        Parameters
        ----------
            state_name : str
                'state_name' child.
        
        """

    def restore_state(self, state_name: str):
        """
        Apply a display state to the active window.
        
        Parameters
        ----------
            state_name : str
                'state_name' child.
        
        """

    def copy(self, state_name: str):
        """
        Create a new display state with settings copied from an existing display state.
        
        Parameters
        ----------
            state_name : str
                'state_name' child.
        
        """

    def read(self, file_name_1: str):
        """
        Read display states from a file.
        
        Parameters
        ----------
            file_name_1 : str
                'file_name' child.
        
        """

    def write(self, file_name: str, state_name: List[str]):
        """
        Write display states to a file.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
            state_name : List
                'state_name' child.
        
        """

    child_object_type: display_states_child = ...
