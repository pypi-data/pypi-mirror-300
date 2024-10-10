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

from .fmg_courant_number import fmg_courant_number as fmg_courant_number_cls
from .enable_fmg_verbose import enable_fmg_verbose as enable_fmg_verbose_cls
from .customize_fmg_initialization import customize_fmg_initialization as customize_fmg_initialization_cls

class fmg_initialization(Group):
    fluent_name = ...
    child_names = ...
    fmg_courant_number: fmg_courant_number_cls = ...
    enable_fmg_verbose: enable_fmg_verbose_cls = ...
    command_names = ...

    def customize_fmg_initialization(self, multi_level_grid: int, residual_reduction_level: List[float | str], cycle_count: List[float | str]):
        """
        'customize_fmg_initialization' command.
        
        Parameters
        ----------
            multi_level_grid : int
                'multi_level_grid' child.
            residual_reduction_level : List
                'residual_reduction_level' child.
            cycle_count : List
                'cycle_count' child.
        
        """

    return_type = ...
