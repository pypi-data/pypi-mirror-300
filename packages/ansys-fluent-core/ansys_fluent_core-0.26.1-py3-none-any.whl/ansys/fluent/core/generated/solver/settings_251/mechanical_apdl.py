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

from .file_name_1 import file_name as file_name_cls
from .thread_name_list import thread_name_list as thread_name_list_cls

class mechanical_apdl(Command):
    """
    Write an Mechanical APDL file.
    
    Parameters
    ----------
        file_name : str
            Enter the desired file name to export.
        thread_name_list : List
            Enter cell zone name list.
    
    """

    fluent_name = "mechanical-apdl"

    argument_names = \
        ['file_name', 'thread_name_list']

    _child_classes = dict(
        file_name=file_name_cls,
        thread_name_list=thread_name_list_cls,
    )

