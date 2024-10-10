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

from .create_7 import create as create_cls
from .delete_1 import delete as delete_cls
from .rename import rename as rename_cls
from .list import list as list_cls
from .list_properties import list_properties as list_properties_cls
from .make_a_copy import make_a_copy as make_a_copy_cls
from .save_1 import save as save_cls
from .load import load as load_cls
from .get_list_of_valid_cell_function_names import get_list_of_valid_cell_function_names as get_list_of_valid_cell_function_names_cls
from .custom_field_functions_child import custom_field_functions_child


class custom_field_functions(NamedObject[custom_field_functions_child], CreatableNamedObjectMixin[custom_field_functions_child]):
    fluent_name = ...
    command_names = ...

    def create(self, name: str, custom_field_function: str):
        """
        Create a custom field function.
        
        Parameters
        ----------
            name : str
                Specify the name for the custom field function.
            custom_field_function : str
                Specify the custom field function.
        
        """

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

    def save(self, filename_1: str):
        """
        Save saving a custom field function to a file.
        
        Parameters
        ----------
            filename_1 : str
                Enter the name you want the file saved with.
        
        """

    def load(self, filename: str):
        """
        Read custom field-function definitions from a file.
        
        Parameters
        ----------
            filename : str
                Enter file name.
        
        """

    query_names = ...

    def get_list_of_valid_cell_function_names(self, ):
        """
        List the names of cell functions that can be used in a custom field function.
        """

    child_object_type: custom_field_functions_child = ...
