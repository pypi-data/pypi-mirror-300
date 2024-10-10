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

from .histogram_1 import histogram as histogram_cls
from .sample_trajectories import sample_trajectories as sample_trajectories_cls
from .zone_types_to_calc_exchange_data_on import zone_types_to_calc_exchange_data_on as zone_types_to_calc_exchange_data_on_cls
from .exch_details_in_dpm_summ_rep_enabled import exch_details_in_dpm_summ_rep_enabled as exch_details_in_dpm_summ_rep_enabled_cls
from .summary import summary as summary_cls
from .extended_summary import extended_summary as extended_summary_cls
from .particle_summary import particle_summary as particle_summary_cls
from .set_per_injection_zone_summaries import set_per_injection_zone_summaries as set_per_injection_zone_summaries_cls

class discrete_phase(Group):
    """
    'discrete_phase' child.
    """

    fluent_name = "discrete-phase"

    child_names = \
        ['histogram', 'sample_trajectories',
         'zone_types_to_calc_exchange_data_on',
         'exch_details_in_dpm_summ_rep_enabled']

    command_names = \
        ['summary', 'extended_summary', 'particle_summary',
         'set_per_injection_zone_summaries']

    _child_classes = dict(
        histogram=histogram_cls,
        sample_trajectories=sample_trajectories_cls,
        zone_types_to_calc_exchange_data_on=zone_types_to_calc_exchange_data_on_cls,
        exch_details_in_dpm_summ_rep_enabled=exch_details_in_dpm_summ_rep_enabled_cls,
        summary=summary_cls,
        extended_summary=extended_summary_cls,
        particle_summary=particle_summary_cls,
        set_per_injection_zone_summaries=set_per_injection_zone_summaries_cls,
    )

    _child_aliases = dict(
        zone_summaries_per_injection="set_per_injection_zone_summaries",
    )

