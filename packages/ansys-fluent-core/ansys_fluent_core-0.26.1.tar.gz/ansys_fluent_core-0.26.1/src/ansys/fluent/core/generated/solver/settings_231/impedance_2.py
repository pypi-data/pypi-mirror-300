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

from .impedance_2_child import impedance_2_child


class impedance_2(ListObject[impedance_2_child]):
    """
    'impedance_2' child.
    """

    fluent_name = "impedance-2"

    child_object_type: impedance_2_child = impedance_2_child
    """
    child_object_type of impedance_2.
    """
    return_type = "<object object at 0x7ff9d1559c40>"
