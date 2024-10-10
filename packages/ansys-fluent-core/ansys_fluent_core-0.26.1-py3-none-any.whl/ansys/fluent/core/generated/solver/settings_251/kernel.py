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


class kernel(Group):
    """
    Deprecated, only for backward compatibility -- objects have been moved one level up.
    """

    fluent_name = "kernel"

    _child_aliases = dict(
        gaussian_factor="../gaussian_factor",
        option="../kernel_type",
    )

