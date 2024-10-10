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

from .reset_statistics import reset_statistics as reset_statistics_cls
from .statistics_controls import statistics_controls as statistics_controls_cls

class statistics(Group):
    fluent_name = ...
    child_names = ...
    reset_statistics: reset_statistics_cls = ...
    command_names = ...

    def statistics_controls(self, method: int, samp_time_period: float | str, samp_time_steps: int, avg_time_period: float | str, avg_time_steps: int):
        """
        Specify statistics parameters of sampling and averaging of flow and optical quantities.
        
        Parameters
        ----------
            method : int
                'method' child.
            samp_time_period : real
                'samp_time_period' child.
            samp_time_steps : int
                'samp_time_steps' child.
            avg_time_period : real
                'avg_time_period' child.
            avg_time_steps : int
                'avg_time_steps' child.
        
        """

    return_type = ...
