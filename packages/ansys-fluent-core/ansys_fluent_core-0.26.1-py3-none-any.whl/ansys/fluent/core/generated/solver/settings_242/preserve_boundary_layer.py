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


class preserve_boundary_layer(String, AllowedValuesMixin):
    """
    0 = Decide at runtime.
    1 = Never preserve.
    2 = Always preserve.
    """

    fluent_name = "preserve-boundary-layer"

