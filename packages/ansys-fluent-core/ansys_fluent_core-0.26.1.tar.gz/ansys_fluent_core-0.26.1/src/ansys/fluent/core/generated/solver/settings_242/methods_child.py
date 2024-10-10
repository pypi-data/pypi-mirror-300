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

from .flow_solver import flow_solver as flow_solver_cls
from .adjoint_solver import adjoint_solver as adjoint_solver_cls
from .adjoint_activation import adjoint_activation as adjoint_activation_cls
from .adjoint_equations import adjoint_equations as adjoint_equations_cls

class methods_child(Group):
    """
    'child_object_type' of methods.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['flow_solver', 'adjoint_solver', 'adjoint_activation',
         'adjoint_equations']

    _child_classes = dict(
        flow_solver=flow_solver_cls,
        adjoint_solver=adjoint_solver_cls,
        adjoint_activation=adjoint_activation_cls,
        adjoint_equations=adjoint_equations_cls,
    )

