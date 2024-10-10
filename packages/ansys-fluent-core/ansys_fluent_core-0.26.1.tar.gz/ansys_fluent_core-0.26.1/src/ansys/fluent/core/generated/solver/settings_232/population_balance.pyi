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

from typing import Union, List, Tuple

from .moments import moments as moments_cls
from .number_density import number_density as number_density_cls

class population_balance(Group):
    fluent_name = ...
    command_names = ...

    def moments(self, surface_list: List[str], volume_list: List[str], num_of_moments: int, write_to_file: bool, filename: str, overwrite: bool):
        """
        Set moments for population balance.
        
        Parameters
        ----------
            surface_list : List
                'surface_list' child.
            volume_list : List
                'volume_list' child.
            num_of_moments : int
                'num_of_moments' child.
            write_to_file : bool
                'write_to_file' child.
            filename : str
                'filename' child.
            overwrite : bool
                'overwrite' child.
        
        """

    def number_density(self, report_type: str, disc_output_type: str, qmom_output_type: str, smm_output_type: str, surface_list: List[str], volume_list: List[str], num_dens_func: str, dia_upper_limit: float | str, file_name: str, overwrite: bool):
        """
        'number_density' command.
        
        Parameters
        ----------
            report_type : str
                'report_type' child.
            disc_output_type : str
                'disc_output_type' child.
            qmom_output_type : str
                'qmom_output_type' child.
            smm_output_type : str
                'smm_output_type' child.
            surface_list : List
                'surface_list' child.
            volume_list : List
                'volume_list' child.
            num_dens_func : str
                'num_dens_func' child.
            dia_upper_limit : real
                'dia_upper_limit' child.
            file_name : str
                'file_name' child.
            overwrite : bool
                'overwrite' child.
        
        """

    return_type = ...
