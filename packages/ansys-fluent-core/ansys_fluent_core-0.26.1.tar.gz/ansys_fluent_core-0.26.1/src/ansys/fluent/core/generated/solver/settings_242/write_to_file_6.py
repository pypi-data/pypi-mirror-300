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

from .param_name import param_name as param_name_cls
from .file_name_29 import file_name as file_name_cls
from .append_data_2 import append_data as append_data_cls

class write_to_file(Command):
    """
    Write parameter value to file.
    
    Parameters
    ----------
        param_name : str
            Enter parameter name.
        file_name : str
            Enter file name.
        append_data : bool
            Enter Yes if you want to append data to file .
    
    """

    fluent_name = "write-to-file"

    argument_names = \
        ['param_name', 'file_name', 'append_data']

    _child_classes = dict(
        param_name=param_name_cls,
        file_name=file_name_cls,
        append_data=append_data_cls,
    )

