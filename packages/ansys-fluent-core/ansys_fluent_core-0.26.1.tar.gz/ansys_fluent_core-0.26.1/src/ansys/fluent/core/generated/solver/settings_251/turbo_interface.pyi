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

from .create_4 import create as create_cls
from .delete_1 import delete as delete_cls
from .rename import rename as rename_cls
from .list import list as list_cls
from .list_properties import list_properties as list_properties_cls
from .make_a_copy import make_a_copy as make_a_copy_cls
from .turbo_interface_child import turbo_interface_child


class turbo_interface(NamedObject[turbo_interface_child], CreatableNamedObjectMixin[turbo_interface_child]):
    fluent_name = ...
    command_names = ...

    def create(self, mesh_interface_name: str, adjacent_cell_zone_1: str, zone1: str, adjacent_cell_zone_2: str, zone2: str, paired_zones: List[str], turbo_choice: str, turbo_non_overlap: bool):
        """
        Create turbo mesh interface.
        
        Parameters
        ----------
            mesh_interface_name : str
                Enter a mesh interface names.
            adjacent_cell_zone_1 : str
                Select adjacent cell zone 1.
            zone1 : str
                Select first interface defining this mesh-interface.
            adjacent_cell_zone_2 : str
                Select adjacent cell zone 2.
            zone2 : str
                Select second interface defining this mesh-interface.
            paired_zones : List
                Paired zones list.
            turbo_choice : str
                Enter your choice of pitch-change types.
            turbo_non_overlap : bool
                Enable non-overlapping walls option for this mesh-interface.
        
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

    child_object_type: turbo_interface_child = ...
