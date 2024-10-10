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
from .network_child import network_child


class network(NamedObject[network_child], CreatableNamedObjectMixinOld[network_child]):
    """
    'network' child.
    """

    fluent_name = "network"

    command_names = \
        ['change_type']

    _child_classes = dict(
        change_type=change_type_cls,
    )

    child_object_type: network_child = network_child
    """
    child_object_type of network.
    """
    return_type = "<object object at 0x7f82c62d01e0>"
