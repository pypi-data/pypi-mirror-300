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

from .coupled_solver import coupled_solver as coupled_solver_cls
from .segregated_solver import segregated_solver as segregated_solver_cls
from .density_based_solver import density_based_solver as density_based_solver_cls

class formulation(Group):
    """
    'formulation' child.
    """

    fluent_name = "formulation"

    child_names = \
        ['coupled_solver', 'segregated_solver', 'density_based_solver']

    _child_classes = dict(
        coupled_solver=coupled_solver_cls,
        segregated_solver=segregated_solver_cls,
        density_based_solver=density_based_solver_cls,
    )

    return_type = "<object object at 0x7f82c5861cc0>"
