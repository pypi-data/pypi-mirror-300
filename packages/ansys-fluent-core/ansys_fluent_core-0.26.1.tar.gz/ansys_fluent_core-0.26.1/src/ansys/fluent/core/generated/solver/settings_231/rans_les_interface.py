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

from .rans_les_interface_child import rans_les_interface_child


class rans_les_interface(NamedObject[rans_les_interface_child], _NonCreatableNamedObjectMixin[rans_les_interface_child]):
    """
    'rans_les_interface' child.
    """

    fluent_name = "rans-les-interface"

    child_object_type: rans_les_interface_child = rans_les_interface_child
    """
    child_object_type of rans_les_interface.
    """
    return_type = "<object object at 0x7ff9d0f87760>"
