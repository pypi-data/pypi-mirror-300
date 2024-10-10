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

from .change_type import change_type as change_type_cls
from .rans_les_interface_child import rans_les_interface_child


class rans_les_interface(NamedObject[rans_les_interface_child], CreatableNamedObjectMixinOld[rans_les_interface_child]):
    """
    'rans_les_interface' child.
    """

    fluent_name = "rans-les-interface"

    command_names = \
        ['change_type']

    _child_classes = dict(
        change_type=change_type_cls,
    )

    child_object_type: rans_les_interface_child = rans_les_interface_child
    """
    child_object_type of rans_les_interface.
    """
    return_type = "<object object at 0x7f82c5df2300>"
