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

from .enable_25 import enable as enable_cls
from .reset_dpm_summaries import reset_dpm_summaries as reset_dpm_summaries_cls

class set_per_injection_zone_summaries(Command):
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

    fluent_name = "set-per-injection-zone-summaries"

    argument_names = \
        ['enable', 'reset_dpm_summaries']

    _child_classes = dict(
        enable=enable_cls,
        reset_dpm_summaries=reset_dpm_summaries_cls,
    )

    _child_aliases = dict(
        summary_state="enable",
    )

