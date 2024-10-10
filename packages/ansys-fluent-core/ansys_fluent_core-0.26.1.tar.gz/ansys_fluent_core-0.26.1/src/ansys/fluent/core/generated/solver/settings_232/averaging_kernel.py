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

from .kernel import kernel as kernel_cls
from .gaussian_factor import gaussian_factor as gaussian_factor_cls

class averaging_kernel(Group):
    """
    'averaging_kernel' child.
    """

    fluent_name = "averaging-kernel"

    child_names = \
        ['kernel', 'gaussian_factor']

    _child_classes = dict(
        kernel=kernel_cls,
        gaussian_factor=gaussian_factor_cls,
    )

    return_type = "<object object at 0x7fe5b9e4d300>"
