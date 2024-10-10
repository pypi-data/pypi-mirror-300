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

from .method_4 import method as method_cls
from .value_5 import value as value_cls
from .piecewise_linear_1 import piecewise_linear as piecewise_linear_cls
from .polynomial_1 import polynomial as polynomial_cls
from .user_defined_5 import user_defined as user_defined_cls

class electrolyte_sigma(Group):
    """
    Set ionic conductivity in electrolyte in the P2D model.
    """

    fluent_name = "electrolyte-sigma"

    child_names = \
        ['method', 'value', 'piecewise_linear', 'polynomial', 'user_defined']

    _child_classes = dict(
        method=method_cls,
        value=value_cls,
        piecewise_linear=piecewise_linear_cls,
        polynomial=polynomial_cls,
        user_defined=user_defined_cls,
    )

