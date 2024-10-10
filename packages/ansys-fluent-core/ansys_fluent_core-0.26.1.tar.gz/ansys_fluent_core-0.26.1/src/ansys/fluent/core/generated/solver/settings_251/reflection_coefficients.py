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

from .normal import normal as normal_cls
from .tangential import tangential as tangential_cls

class reflection_coefficients(Group):
    """
    Discrete Phase Wall Reflection Coefficients.
    """

    fluent_name = "reflection-coefficients"

    child_names = \
        ['normal', 'tangential']

    _child_classes = dict(
        normal=normal_cls,
        tangential=tangential_cls,
    )

    _child_aliases = dict(
        dpm_bc_norm_coeff="normal",
        dpm_bc_tang_coeff="tangential",
    )

