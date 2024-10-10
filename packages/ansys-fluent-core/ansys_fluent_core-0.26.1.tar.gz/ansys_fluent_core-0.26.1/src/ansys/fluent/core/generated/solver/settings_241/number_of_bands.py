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

from .set_all_interfaces import set_all_interfaces as set_all_interfaces_cls
from .set_specific_interface import set_specific_interface as set_specific_interface_cls

class number_of_bands(Group):
    """
    Set the maximum number of bands to be used for mixing.
    """

    fluent_name = "number-of-bands"

    child_names = \
        ['set_all_interfaces']

    command_names = \
        ['set_specific_interface']

    _child_classes = dict(
        set_all_interfaces=set_all_interfaces_cls,
        set_specific_interface=set_specific_interface_cls,
    )

    return_type = "<object object at 0x7fd93fba67f0>"
