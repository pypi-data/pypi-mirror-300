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

from .total_temperature_1 import total_temperature as total_temperature_cls

class thermal(Group):
    """
    Help not available.
    """

    fluent_name = "thermal"

    child_names = \
        ['total_temperature']

    _child_classes = dict(
        total_temperature=total_temperature_cls,
    )

    _child_aliases = dict(
        t0="total_temperature",
    )

