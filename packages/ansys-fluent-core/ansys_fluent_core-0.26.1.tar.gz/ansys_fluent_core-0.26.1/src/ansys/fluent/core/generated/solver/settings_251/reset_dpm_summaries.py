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


class reset_dpm_summaries(Boolean):
    """
    Disabling the per-injection per-zone DPM summary reports requires that
    both the current DPM summary report data are reset and all particle
    parcels currently in the domain are cleared out(!).
    Set this command argument / check this checkbox to
    confirm that you want to proceed as described.
    """

    fluent_name = "reset-dpm-summaries"

