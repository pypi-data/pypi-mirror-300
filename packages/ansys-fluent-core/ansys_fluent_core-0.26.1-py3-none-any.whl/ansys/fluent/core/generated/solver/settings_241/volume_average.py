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

from .cell_zones_6 import cell_zones as cell_zones_cls
from .cell_function_1 import cell_function as cell_function_cls
from .current_domain import current_domain as current_domain_cls
from .write_to_file_1 import write_to_file as write_to_file_cls
from .file_name_1 import file_name as file_name_cls
from .append_data import append_data as append_data_cls

class volume_average(Command):
    """
    Print volume-weighted average of scalar over specified cell zones.
    
    Parameters
    ----------
        cell_zones : List
            Volume id/name.
        cell_function : str
            Specify Field.
        current_domain : str
            'current_domain' child.
        write_to_file : bool
            'write_to_file' child.
        file_name : str
            'file_name' child.
        append_data : bool
            'append_data' child.
    
    """

    fluent_name = "volume-average"

    argument_names = \
        ['cell_zones', 'cell_function', 'current_domain', 'write_to_file',
         'file_name', 'append_data']

    _child_classes = dict(
        cell_zones=cell_zones_cls,
        cell_function=cell_function_cls,
        current_domain=current_domain_cls,
        write_to_file=write_to_file_cls,
        file_name=file_name_cls,
        append_data=append_data_cls,
    )

    return_type = "<object object at 0x7fd93f7cb6f0>"
