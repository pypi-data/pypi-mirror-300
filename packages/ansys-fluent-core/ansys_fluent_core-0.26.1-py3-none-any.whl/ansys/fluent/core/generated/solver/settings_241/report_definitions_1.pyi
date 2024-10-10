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
from .print_to_console import print_to_console as print_to_console_cls
from .write_to_file_2 import write_to_file as write_to_file_cls
from .report_definitions_child import report_definitions_child


class report_definitions(NamedObject[report_definitions_child], CreatableNamedObjectMixinOld[report_definitions_child]):
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

    def print_to_console(self, name: str):
        """
        Print parameter value to console.
        
        Parameters
        ----------
            name : str
                'name' child.
        
        """

    def write_to_file(self, param_name: str, file_name: str, append_data: bool):
        """
        Write parameter value to file.
        
        Parameters
        ----------
            param_name : str
                'param_name' child.
            file_name : str
                'file_name' child.
            append_data : bool
                'append_data' child.
        
        """

    child_object_type: report_definitions_child = ...
    return_type = ...
