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

from .multi_stage_child import multi_stage_child


class multi_stage(ListObject[multi_stage_child]):
    """
    'multi_stage' child.
    """

    fluent_name = "multi-stage"

    child_object_type: multi_stage_child = multi_stage_child
    """
    child_object_type of multi_stage.
    """
    return_type = "<object object at 0x7ff9d0b7b0a0>"
