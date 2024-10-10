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

from .histogram_1 import histogram as histogram_cls
from .sample_trajectories import sample_trajectories as sample_trajectories_cls
from .zone_types_to_calc_exchange_data_on import zone_types_to_calc_exchange_data_on as zone_types_to_calc_exchange_data_on_cls
from .exch_details_in_dpm_summ_rep_enabled import exch_details_in_dpm_summ_rep_enabled as exch_details_in_dpm_summ_rep_enabled_cls
from .summary import summary as summary_cls
from .extended_summary import extended_summary as extended_summary_cls
from .particle_summary import particle_summary as particle_summary_cls
from .set_per_injection_zone_summaries import set_per_injection_zone_summaries as set_per_injection_zone_summaries_cls

class discrete_phase(Group):
    fluent_name = ...
    child_names = ...
    histogram: histogram_cls = ...
    sample_trajectories: sample_trajectories_cls = ...
    zone_types_to_calc_exchange_data_on: zone_types_to_calc_exchange_data_on_cls = ...
    exch_details_in_dpm_summ_rep_enabled: exch_details_in_dpm_summ_rep_enabled_cls = ...
    command_names = ...

    def summary(self, ):
        """
        Print discrete phase summary report of particle fates.
        """

    def extended_summary(self, write_to_file: bool, file_name: str, include_in_domain_particles: bool, pick_injection: bool, injection: str):
        """
        Print extended discrete phase summary report of particle fates, with options.
        
        Parameters
        ----------
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            include_in_domain_particles : bool
                Specify whether to include particle parcels that are currently in the domain in the report.
        This may take some extra time for the report to be prepared.
            pick_injection : bool
                'pick_injection' child.
            injection : str
                'injection' child.
        
        """

    def particle_summary(self, injection_names: List[str]):
        """
        Print summary report for all current particles.
        
        Parameters
        ----------
            injection_names : List
                Specify the injection[s] whose in-domain particle parcels are to be included in the report.
        
        """

    def set_per_injection_zone_summaries(self, enable: bool, reset_dpm_summaries: bool):
        """
        Enable per-injection per-zone DPM summary reports.
        
        Parameters
        ----------
            enable : bool
                Specify whether to enable or disable the per-injection per-zone DPM summary reports.
        Enabling them will mean that more memory will be used to hold the data being collected.
        For unsteady tracking, if some data for DPM summary reports have already been collected,
        they will continue to be shown just specific to the zone, not any injection, while
        data collected in the future will be shown both zone- and injection-specific.
        Disabling requires that both the current DPM summary report data are reset
        and all particle parcels currently in the domain are cleared out(!).
            reset_dpm_summaries : bool
                Disabling the per-injection per-zone DPM summary reports requires that
        both the current DPM summary report data are reset and all particle
        parcels currently in the domain are cleared out(!).
        Set this command argument / check this checkbox to
        confirm that you want to proceed as described.
        
        """

