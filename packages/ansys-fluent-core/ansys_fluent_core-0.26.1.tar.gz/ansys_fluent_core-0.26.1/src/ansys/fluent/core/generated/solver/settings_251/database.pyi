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

from .database_type import database_type as database_type_cls
from .copy_by_formula import copy_by_formula as copy_by_formula_cls
from .copy_by_name import copy_by_name as copy_by_name_cls
from .list_materials import list_materials as list_materials_cls
from .list_properties_2 import list_properties as list_properties_cls

class database(Group):
    fluent_name = ...
    child_names = ...
    database_type: database_type_cls = ...
    command_names = ...

    def copy_by_formula(self, type: str, formula: str, new_name: str, new_formula: str):
        """
        Copy database material by formula.
        
        Parameters
        ----------
            type : str
                'type' child.
            formula : str
                'formula' child.
            new_name : str
                Material with same name exist. Please select new material name.
            new_formula : str
                Material with same chemical formula exist. Please select new chemical formula.
        
        """

    def copy_by_name(self, type: str, name: str, new_name: str, new_formula: str):
        """
        Copy database material by name.
        
        Parameters
        ----------
            type : str
                'type' child.
            name : str
                'name' child.
            new_name : str
                Material with same name exist. Please select new material name.
            new_formula : str
                Material with same chemical formula exist. Please select new chemical formula.
        
        """

    def list_materials(self, ):
        """
        List database materials.
        """

    def list_properties(self, name: str):
        """
        List database material properties.
        
        Parameters
        ----------
            name : str
                'name' child.
        
        """

