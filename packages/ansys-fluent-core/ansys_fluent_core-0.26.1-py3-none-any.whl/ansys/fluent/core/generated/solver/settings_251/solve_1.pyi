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

from .iterate_1 import iterate as iterate_cls
from .dual_time_iterate_1 import dual_time_iterate as dual_time_iterate_cls

class solve(Group):
    fluent_name = ...
    command_names = ...

    def iterate(self, iter_count: int, time_steps_count: int, iter_per_time_step_count: int):
        """
        Iteration the multidomain conjugate heat transfer.
        
        Parameters
        ----------
            iter_count : int
                'iter_count' child.
            time_steps_count : int
                'time_steps_count' child.
            iter_per_time_step_count : int
                'iter_per_time_step_count' child.
        
        """

    def dual_time_iterate(self, iter_count: int, time_steps_count: int, iter_per_time_step_count: int):
        """
        Dual-time iterate the multidomain conjugate heat transfer.
        
        Parameters
        ----------
            iter_count : int
                'iter_count' child.
            time_steps_count : int
                'time_steps_count' child.
            iter_per_time_step_count : int
                'iter_per_time_step_count' child.
        
        """

