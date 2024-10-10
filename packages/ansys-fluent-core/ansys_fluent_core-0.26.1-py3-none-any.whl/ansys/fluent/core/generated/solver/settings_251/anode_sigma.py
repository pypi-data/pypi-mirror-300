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

from .option_21 import option as option_cls
from .value_7 import value as value_cls
from .piecewise_linear import piecewise_linear as piecewise_linear_cls
from .polynomial import polynomial as polynomial_cls
from .user_defined_12 import user_defined as user_defined_cls

class anode_sigma(Group):
    """
    Set solid electric conductivity in anode in the P2D model.
    """

    fluent_name = "anode-sigma"

    child_names = \
        ['option', 'value', 'piecewise_linear', 'polynomial', 'user_defined']

    _child_classes = dict(
        option=option_cls,
        value=value_cls,
        piecewise_linear=piecewise_linear_cls,
        polynomial=polynomial_cls,
        user_defined=user_defined_cls,
    )

    _child_aliases = dict(
        method="option",
    )

