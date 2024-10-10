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

from .enabled_20 import enabled as enabled_cls
from .file_name_10 import file_name as file_name_cls

class write_all_data_table(Command):
    """
    Command to write all ECM data tables.
    
    Parameters
    ----------
        enabled : bool
            Write all ECM data tables.
        file_name : str
            File name in writing ECM tables.
    
    """

    fluent_name = "write-all-data-table"

    argument_names = \
        ['enabled', 'file_name']

    _child_classes = dict(
        enabled=enabled_cls,
        file_name=file_name_cls,
    )

