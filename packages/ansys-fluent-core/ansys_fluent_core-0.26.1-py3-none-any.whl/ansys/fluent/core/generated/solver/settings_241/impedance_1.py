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

from .list_properties import list_properties as list_properties_cls
from .impedance_1_child import impedance_1_child


class impedance_1(ListObject[impedance_1_child]):
    """
    Real Pole Series.
    """

    fluent_name = "impedance-1"

    command_names = \
        ['list_properties']

    _child_classes = dict(
        list_properties=list_properties_cls,
    )

    child_object_type: impedance_1_child = impedance_1_child
    """
    child_object_type of impedance_1.
    """
    return_type = "<object object at 0x7fd94cf65710>"
