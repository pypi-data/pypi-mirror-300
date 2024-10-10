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
from .volumes_2 import volumes as volumes_cls
from .cell_function_2 import cell_function as cell_function_cls
from .current_domain import current_domain as current_domain_cls
from .write_to_file_2 import write_to_file as write_to_file_cls
from .file_name_14 import file_name as file_name_cls
from .append_data import append_data as append_data_cls

class twopisum(Command):
    """
    Print sum of scalar over specified cell zones multiplied by 2\\*Pi.
    
    Parameters
    ----------
        cell_zones : List
            Volume id/name.
        volumes : List
            UTL Volume name.
        cell_function : str
            Specify Field.
        current_domain : str
            Select the domain.
        write_to_file : bool
            Choose whether or not to write to a file.
        file_name : str
            Enter the name you want the file saved with.
        append_data : bool
            Choose whether or not to append data to existing file.
    
    """

    fluent_name = "twopisum"

    argument_names = \
        ['cell_zones', 'volumes', 'cell_function', 'current_domain',
         'write_to_file', 'file_name', 'append_data']

    _child_classes = dict(
        cell_zones=cell_zones_cls,
        volumes=volumes_cls,
        cell_function=cell_function_cls,
        current_domain=current_domain_cls,
        write_to_file=write_to_file_cls,
        file_name=file_name_cls,
        append_data=append_data_cls,
    )

