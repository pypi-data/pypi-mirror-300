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


class oil_flow(Boolean):
    """
    Toggles between regular pathlines and oil-flow pathlines. When this option is selected, pathlines are constrained to lie on the zone(s) selected in the On Zone list.
    """

    fluent_name = "oil-flow"

