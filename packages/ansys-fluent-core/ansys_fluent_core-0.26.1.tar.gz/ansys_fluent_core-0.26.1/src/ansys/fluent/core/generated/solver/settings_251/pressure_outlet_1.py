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

from .blending_factor_1 import blending_factor as blending_factor_cls
from .bin_count import bin_count as bin_count_cls
from .average_pressure import average_pressure as average_pressure_cls

class pressure_outlet(Group):
    """
    Select pressure specification method on pressure-outlet boundaries.
    """

    fluent_name = "pressure-outlet"

    child_names = \
        ['blending_factor', 'bin_count', 'average_pressure']

    _child_classes = dict(
        blending_factor=blending_factor_cls,
        bin_count=bin_count_cls,
        average_pressure=average_pressure_cls,
    )

