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


class direction_option(String, AllowedValuesMixin):
    """
    Select the axis you are specifying using by selecting either X, Y, or Z. You can either specify the orientation by providing a point or a direction.
    """

    fluent_name = "direction-option"

