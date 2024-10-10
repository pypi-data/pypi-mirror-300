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

from .options_11 import options as options_cls
from .domain_val import domain_val as domain_val_cls
from .all_wall_zones import all_wall_zones as all_wall_zones_cls
from .wall_thread_list import wall_thread_list as wall_thread_list_cls
from .direction_vector_1 import direction_vector as direction_vector_cls
from .momentum_center import momentum_center as momentum_center_cls
from .momentum_axis import momentum_axis as momentum_axis_cls
from .pressure_coordinate import pressure_coordinate as pressure_coordinate_cls
from .coord_val import coord_val as coord_val_cls
from .write_to_file import write_to_file as write_to_file_cls
from .file_name_1 import file_name as file_name_cls
from .append_data import append_data as append_data_cls
from .overwrite import overwrite as overwrite_cls

class forces(Command):
    """
    'forces' command.
    
    Parameters
    ----------
        options : str
            'options' child.
        domain_val : str
            'domain_val' child.
        all_wall_zones : bool
            Select all wall zones available.
        wall_thread_list : List
            'wall_thread_list' child.
        direction_vector : Tuple
            'direction_vector' child.
        momentum_center : Tuple
            'momentum_center' child.
        momentum_axis : Tuple
            'momentum_axis' child.
        pressure_coordinate : str
            'pressure_coordinate' child.
        coord_val : real
            'coord_val' child.
        write_to_file : bool
            'write_to_file' child.
        file_name : str
            'file_name' child.
        append_data : bool
            'append_data' child.
        overwrite : bool
            'overwrite' child.
    
    """

    fluent_name = "forces"

    argument_names = \
        ['options', 'domain_val', 'all_wall_zones', 'wall_thread_list',
         'direction_vector', 'momentum_center', 'momentum_axis',
         'pressure_coordinate', 'coord_val', 'write_to_file', 'file_name',
         'append_data', 'overwrite']

    _child_classes = dict(
        options=options_cls,
        domain_val=domain_val_cls,
        all_wall_zones=all_wall_zones_cls,
        wall_thread_list=wall_thread_list_cls,
        direction_vector=direction_vector_cls,
        momentum_center=momentum_center_cls,
        momentum_axis=momentum_axis_cls,
        pressure_coordinate=pressure_coordinate_cls,
        coord_val=coord_val_cls,
        write_to_file=write_to_file_cls,
        file_name=file_name_cls,
        append_data=append_data_cls,
        overwrite=overwrite_cls,
    )

    return_type = "<object object at 0x7ff9d083cc00>"
