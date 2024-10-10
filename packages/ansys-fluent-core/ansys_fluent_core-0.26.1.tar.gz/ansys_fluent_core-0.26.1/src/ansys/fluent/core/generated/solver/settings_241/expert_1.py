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

from .parallel_verbosity_level import parallel_verbosity_level as parallel_verbosity_level_cls
from .crossover_tolerance import crossover_tolerance as crossover_tolerance_cls

class expert(Group):
    """
    'expert' child.
    """

    fluent_name = "expert"

    child_names = \
        ['parallel_verbosity_level', 'crossover_tolerance']

    _child_classes = dict(
        parallel_verbosity_level=parallel_verbosity_level_cls,
        crossover_tolerance=crossover_tolerance_cls,
    )

    return_type = "<object object at 0x7fd94d0e5e30>"
