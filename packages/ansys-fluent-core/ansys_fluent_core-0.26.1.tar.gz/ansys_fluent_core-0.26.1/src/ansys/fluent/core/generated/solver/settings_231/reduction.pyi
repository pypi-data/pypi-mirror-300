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

from .setup_reduction import setup_reduction as setup_reduction_cls
from .pick_sample_to_reduce import pick_sample_to_reduce as pick_sample_to_reduce_cls
from .reduce_picked_sample import reduce_picked_sample as reduce_picked_sample_cls

class reduction(Group):
    fluent_name = ...
    child_names = ...
    setup_reduction: setup_reduction_cls = ...
    command_names = ...

    def pick_sample_to_reduce(self, change_curr_sample: bool, sample: str):
        """
        Pick a sample for which to first set-up and then perform the data reduction.
        
        Parameters
        ----------
            change_curr_sample : bool
                'change_curr_sample' child.
            sample : str
                'sample' child.
        
        """

    def reduce_picked_sample(self, check_reduction_wt: bool, file_name: str, overwrite: bool):
        """
        Reduce a sample after first picking it and setting up all data-reduction options and parameters.
        
        Parameters
        ----------
            check_reduction_wt : bool
                'check_reduction_wt' child.
            file_name : str
                'file_name' child.
            overwrite : bool
                'overwrite' child.
        
        """

    return_type = ...
