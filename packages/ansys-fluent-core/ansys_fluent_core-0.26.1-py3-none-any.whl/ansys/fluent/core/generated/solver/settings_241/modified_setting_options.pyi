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

from .modified_setting import modified_setting as modified_setting_cls
from .write_user_setting import write_user_setting as write_user_setting_cls

class modified_setting_options(Group):
    fluent_name = ...
    command_names = ...

    def modified_setting(self, setting_type: List[str]):
        """
        Specify which settings will be checked for non-default status for generating the Modified Settings Summary table.
        
        Parameters
        ----------
            setting_type : List
                'setting_type' child.
        
        """

    def write_user_setting(self, file_name: str):
        """
        Write the contents of the Modified Settings Summary table to a file.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
        
        """

    return_type = ...
