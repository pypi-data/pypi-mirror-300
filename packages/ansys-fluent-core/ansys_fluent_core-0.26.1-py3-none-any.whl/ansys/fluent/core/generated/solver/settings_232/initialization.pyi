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

from .initialization_type import initialization_type as initialization_type_cls
from .reference_frame_1 import reference_frame as reference_frame_cls
from .defaults import defaults as defaults_cls
from .fmg_options import fmg_options as fmg_options_cls
from .localized_turb_init import localized_turb_init as localized_turb_init_cls
from .hybrid_init_options import hybrid_init_options as hybrid_init_options_cls
from .patch import patch as patch_cls
from .open_channel_auto_init import open_channel_auto_init as open_channel_auto_init_cls
from .fmg_initialization import fmg_initialization as fmg_initialization_cls
from .initialize import initialize as initialize_cls
from .compute_defaults import compute_defaults as compute_defaults_cls
from .fmg_initialize import fmg_initialize as fmg_initialize_cls
from .standard_initialize import standard_initialize as standard_initialize_cls
from .hybrid_initialize import hybrid_initialize as hybrid_initialize_cls
from .list_defaults import list_defaults as list_defaults_cls
from .init_turb_vel_fluctuations import init_turb_vel_fluctuations as init_turb_vel_fluctuations_cls
from .init_flow_statistics import init_flow_statistics as init_flow_statistics_cls
from .show_iterations_sampled import show_iterations_sampled as show_iterations_sampled_cls
from .show_time_sampled import show_time_sampled as show_time_sampled_cls
from .dpm_reset import dpm_reset as dpm_reset_cls
from .lwf_reset import lwf_reset as lwf_reset_cls
from .init_acoustics_options import init_acoustics_options as init_acoustics_options_cls
from .levelset_auto_init import levelset_auto_init as levelset_auto_init_cls

class initialization(Group):
    fluent_name = ...
    child_names = ...
    initialization_type: initialization_type_cls = ...
    reference_frame: reference_frame_cls = ...
    defaults: defaults_cls = ...
    fmg_options: fmg_options_cls = ...
    localized_turb_init: localized_turb_init_cls = ...
    hybrid_init_options: hybrid_init_options_cls = ...
    patch: patch_cls = ...
    open_channel_auto_init: open_channel_auto_init_cls = ...
    fmg_initialization: fmg_initialization_cls = ...
    command_names = ...

    def initialize(self, ):
        """
        'initialize' command.
        """

    def compute_defaults(self, from_zone_type: str, from_zone_name: str, phase: str):
        """
        'compute_defaults' command.
        
        Parameters
        ----------
            from_zone_type : str
                'from_zone_type' child.
            from_zone_name : str
                'from_zone_name' child.
            phase : str
                'phase' child.
        
        """

    def fmg_initialize(self, ):
        """
        Initialize using the full-multigrid initialization (FMG).
        """

    def standard_initialize(self, ):
        """
        Initialize the flow field with the current default values.
        """

    def hybrid_initialize(self, ):
        """
        Initialize using the hybrid initialization method.
        """

    def list_defaults(self, ):
        """
        List default values.
        """

    def init_turb_vel_fluctuations(self, ):
        """
        Initialize turbulent velocity fluctuations.
        """

    def init_flow_statistics(self, ):
        """
        Initialize statistics.
        """

    def show_iterations_sampled(self, ):
        """
        'show_iterations_sampled' command.
        """

    def show_time_sampled(self, ):
        """
        Display the amount of simulated time covered by the data sampled for unsteady statistics.
        """

    def dpm_reset(self, ):
        """
        Reset discrete phase source terms to zero.
        """

    def lwf_reset(self, ):
        """
        Delete wall film particles and initialize wall film variables to zero.
        """

    def init_acoustics_options(self, set_ramping_length: bool, time_step_count: int):
        """
        'init_acoustics_options' command.
        
        Parameters
        ----------
            set_ramping_length : bool
                Enable/Disable ramping length and initialize acoustics.
            time_step_count : int
                Set number of timesteps for ramping of sources.
        
        """

    def levelset_auto_init(self, ):
        """
        'levelset_auto_init' command.
        """

    return_type = ...
