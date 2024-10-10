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


class enable(Boolean):
    """
    Specify whether to enable or disable the per-injection per-zone DPM summary reports.
    Enabling them will mean that more memory will be used to hold the data being collected.
    For unsteady tracking, if some data for DPM summary reports have already been collected,
    they will continue to be shown just specific to the zone, not any injection, while
    data collected in the future will be shown both zone- and injection-specific.
    Disabling requires that both the current DPM summary report data are reset
    and all particle parcels currently in the domain are cleared out(!).
    """

    fluent_name = "enable?"

