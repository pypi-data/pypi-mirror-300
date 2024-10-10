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
from .intake_fan_child import intake_fan_child


class intake_fan(NamedObject[intake_fan_child], CreatableNamedObjectMixinOld[intake_fan_child]):
    """
    'intake_fan' child.
    """

    fluent_name = "intake-fan"

    command_names = \
        ['change_type']

    _child_classes = dict(
        change_type=change_type_cls,
    )

    child_object_type: intake_fan_child = intake_fan_child
    """
    child_object_type of intake_fan.
    """
    return_type = "<object object at 0x7f82c667cbf0>"
