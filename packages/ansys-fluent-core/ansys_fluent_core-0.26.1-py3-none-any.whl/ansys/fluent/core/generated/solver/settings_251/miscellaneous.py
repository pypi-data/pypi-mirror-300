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

from .compute_statistics import compute_statistics as compute_statistics_cls
from .statistics_level import statistics_level as statistics_level_cls

class miscellaneous(Group):
    """
    Enter flexible numeris menu for solution statics options.
    """

    fluent_name = "miscellaneous"

    child_names = \
        ['compute_statistics', 'statistics_level']

    _child_classes = dict(
        compute_statistics=compute_statistics_cls,
        statistics_level=statistics_level_cls,
    )

