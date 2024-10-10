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
from .outflow_child import outflow_child


class outflow(NamedObject[outflow_child], CreatableNamedObjectMixinOld[outflow_child]):
    """
    'outflow' child.
    """

    fluent_name = "outflow"

    command_names = \
        ['change_type']

    _child_classes = dict(
        change_type=change_type_cls,
    )

    child_object_type: outflow_child = outflow_child
    """
    child_object_type of outflow.
    """
    return_type = "<object object at 0x7f82c62d0520>"
