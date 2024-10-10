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

from .file_name import file_name as file_name_cls

class write_sc_file(Command):
    """
    Write a Fluent Input File for System Coupling.
    
    Parameters
    ----------
        file_name : str
            Enter the desired file name to export.
    
    """

    fluent_name = "write-sc-file"

    argument_names = \
        ['file_name']

    _child_classes = dict(
        file_name=file_name_cls,
    )

