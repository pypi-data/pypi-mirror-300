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

from .use_weighting import use_weighting as use_weighting_cls
from .make_steady_from_unsteady_file import make_steady_from_unsteady_file as make_steady_from_unsteady_file_cls
from .weighting_variable import weighting_variable as weighting_variable_cls
from .reset_min_and_max import reset_min_and_max as reset_min_and_max_cls
from .set_minimum import set_minimum as set_minimum_cls
from .set_maximum import set_maximum as set_maximum_cls
from .use_logarithmic import use_logarithmic as use_logarithmic_cls
from .number_of_bins import number_of_bins as number_of_bins_cls
from .all_variables_number_of_bins import all_variables_number_of_bins as all_variables_number_of_bins_cls
from .list_settings import list_settings as list_settings_cls

class setup_reduction(Group):
    fluent_name = ...
    child_names = ...
    use_weighting: use_weighting_cls = ...
    make_steady_from_unsteady_file: make_steady_from_unsteady_file_cls = ...
    command_names = ...

    def weighting_variable(self, change_curr_sample: bool, sample: str):
        """
        Choose the weighting variable for the averaging in each bin in the data reduction.
        
        Parameters
        ----------
            change_curr_sample : bool
                'change_curr_sample' child.
            sample : str
                'sample' child.
        
        """

    def reset_min_and_max(self, sample_var: str, reset_range: bool):
        """
        Reset the min and max values of the range to be considered for a specific variable in the data reduction.
        
        Parameters
        ----------
            sample_var : str
                'sample_var' child.
            reset_range : bool
                'reset_range' child.
        
        """

    def set_minimum(self, sample_var: str, min_val: float | str):
        """
        Set the minimum value of the range to be considered for a specific variable in the data reduction.
        
        Parameters
        ----------
            sample_var : str
                'sample_var' child.
            min_val : real
                'min_val' child.
        
        """

    def set_maximum(self, sample_var: str, max_val: float | str):
        """
        'set_maximum' command.
        
        Parameters
        ----------
            sample_var : str
                'sample_var' child.
            max_val : real
                'max_val' child.
        
        """

    def use_logarithmic(self, sample_var: str, enable_log: bool):
        """
        Switch on or off logarithmic scaling to be used for a specific variable in the data reduction.
        
        Parameters
        ----------
            sample_var : str
                'sample_var' child.
            enable_log : bool
                'enable_log' child.
        
        """

    def number_of_bins(self, sample_var: str, num_bins: int):
        """
        Set the number of bins to be used for a specific variable in the data reduction.
        
        Parameters
        ----------
            sample_var : str
                'sample_var' child.
            num_bins : int
                'num_bins' child.
        
        """

    def all_variables_number_of_bins(self, all_var_num_of_bins: int):
        """
        Set the number of bins to be used for ALL variables in the data reduction.
        
        Parameters
        ----------
            all_var_num_of_bins : int
                'all_var_num_of_bins' child.
        
        """

    def list_settings(self, ):
        """
        List all user inputs for the sample picked for data reduction.
        """

    return_type = ...
