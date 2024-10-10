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
from .fluid_child_1 import fluid_child


class fluid(NamedObject[fluid_child], CreatableNamedObjectMixinOld[fluid_child]):
    """
    'fluid' child.
    """

    fluent_name = "fluid"

    command_names = \
        ['change_type']

    _child_classes = dict(
        change_type=change_type_cls,
    )

    child_object_type: fluid_child = fluid_child
    """
    child_object_type of fluid.
    """
    return_type = "<object object at 0x7f82c6a0de20>"
