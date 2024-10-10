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

from .write_to_file_1 import write_to_file as write_to_file_cls
from .file_name_2 import file_name as file_name_cls

class summary(Command):
    """
    Print report summary.
    
    Parameters
    ----------
        write_to_file : bool
            'write_to_file' child.
        file_name : str
            'file_name' child.
    
    """

    fluent_name = "summary"

    argument_names = \
        ['write_to_file', 'file_name']

    _child_classes = dict(
        write_to_file=write_to_file_cls,
        file_name=file_name_cls,
    )

