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

from .domain_2 import domain as domain_cls
from .zones_7 import zones as zones_cls
from .physics_1 import physics as physics_cls
from .write_to_file_2 import write_to_file as write_to_file_cls
from .file_name_14 import file_name as file_name_cls
from .append_data import append_data as append_data_cls

class heat_transfer(Command):
    """
    Print heat transfer rate at boundaries.
    
    Parameters
    ----------
        domain : str
            Select the domain.
        zones : List
            Enter zone name list.
        physics : List
            'physics' child.
        write_to_file : bool
            Choose whether or not to write to a file.
        file_name : str
            Enter the name you want the file saved with.
        append_data : bool
            Choose whether or not to append data to existing file.
    
    """

    fluent_name = "heat-transfer"

    argument_names = \
        ['domain', 'zones', 'physics', 'write_to_file', 'file_name',
         'append_data']

    _child_classes = dict(
        domain=domain_cls,
        zones=zones_cls,
        physics=physics_cls,
        write_to_file=write_to_file_cls,
        file_name=file_name_cls,
        append_data=append_data_cls,
    )

