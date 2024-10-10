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


class option(Boolean):
    """
    Enable/disable virtual mass force acting on particles. This force term may be important if the particle density is equal to or less than the local fluid density.
    """

    fluent_name = "option"

    return_type = "<object object at 0x7fe5b9e4d540>"
