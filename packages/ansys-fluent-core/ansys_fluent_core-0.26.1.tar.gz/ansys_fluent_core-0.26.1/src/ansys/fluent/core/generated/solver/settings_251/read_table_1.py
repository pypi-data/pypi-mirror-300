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

from .file_name_1_6 import file_name_1 as file_name_1_cls

class read_table(Command):
    """
    3D Reading table command.
    
    Parameters
    ----------
        file_name_1 : str
            Set file name in the 3D table-reading command.
    
    """

    fluent_name = "read-table"

    argument_names = \
        ['file_name']

    _child_classes = dict(
        file_name=file_name_1_cls,
    )

