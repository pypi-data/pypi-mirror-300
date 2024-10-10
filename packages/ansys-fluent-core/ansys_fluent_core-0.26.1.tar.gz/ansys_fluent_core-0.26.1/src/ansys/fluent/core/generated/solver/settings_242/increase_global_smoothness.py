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


class increase_global_smoothness(Boolean):
    """
    When enabled, more global control points will be used to improve the smoothness of the deformation. Enabling this option may increase memory cost and computational time.
    """

    fluent_name = "increase-global-smoothness"

