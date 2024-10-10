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

from .max_fine_relaxations import max_fine_relaxations as max_fine_relaxations_cls
from .max_coarse_relaxations import max_coarse_relaxations as max_coarse_relaxations_cls

class flexible_cycle_paramters(Group):
    """
    'flexible_cycle_paramters' child.
    """

    fluent_name = "flexible-cycle-paramters"

    child_names = \
        ['max_fine_relaxations', 'max_coarse_relaxations']

    _child_classes = dict(
        max_fine_relaxations=max_fine_relaxations_cls,
        max_coarse_relaxations=max_coarse_relaxations_cls,
    )

    return_type = "<object object at 0x7f82c5860720>"
