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
from .recirculation_inlet_child import recirculation_inlet_child


class recirculation_inlet(NamedObject[recirculation_inlet_child], CreatableNamedObjectMixinOld[recirculation_inlet_child]):
    """
    'recirculation_inlet' child.
    """

    fluent_name = "recirculation-inlet"

    command_names = \
        ['change_type']

    _child_classes = dict(
        change_type=change_type_cls,
    )

    child_object_type: recirculation_inlet_child = recirculation_inlet_child
    """
    child_object_type of recirculation_inlet.
    """
    return_type = "<object object at 0x7f82c5df24e0>"
