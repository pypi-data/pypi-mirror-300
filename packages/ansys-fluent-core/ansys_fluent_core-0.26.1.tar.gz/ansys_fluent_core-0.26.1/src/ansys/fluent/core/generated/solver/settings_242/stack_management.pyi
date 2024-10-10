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

from .list_fc_units import list_fc_units as list_fc_units_cls
from .stack_create_fcu import stack_create_fcu as stack_create_fcu_cls
from .stack_modify_fcu import stack_modify_fcu as stack_modify_fcu_cls
from .stack_delete_fcu import stack_delete_fcu as stack_delete_fcu_cls
from .stack_reset_fcu import stack_reset_fcu as stack_reset_fcu_cls
from .stack_submit_fcu import stack_submit_fcu as stack_submit_fcu_cls

class stack_management(Group):
    fluent_name = ...
    command_names = ...

    def list_fc_units(self, ):
        """
        List fuel cell units.
        """

    def stack_create_fcu(self, fcu_name: str, cellzones: List[str]):
        """
        Create stack units.
        
        Parameters
        ----------
            fcu_name : str
                'fcu_name' child.
            cellzones : List
                Enter cell zone name list.
        
        """

    def stack_modify_fcu(self, fcu_name: str, cellzones: List[str]):
        """
        Modify stack units.
        
        Parameters
        ----------
            fcu_name : str
                'fcu_name' child.
            cellzones : List
                Enter cell zone name list.
        
        """

    def stack_delete_fcu(self, fcu_name: str):
        """
        Delete stack units.
        
        Parameters
        ----------
            fcu_name : str
                'fcu_name' child.
        
        """

    def stack_reset_fcu(self, reset: bool):
        """
        Reset stack units.
        
        Parameters
        ----------
            reset : bool
                'reset' child.
        
        """

    def stack_submit_fcu(self, submit: bool):
        """
        Apply stack units settings.
        
        Parameters
        ----------
            submit : bool
                'submit' child.
        
        """

