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
from .multi_stage_child import multi_stage_child


class multi_stage(ListObject[multi_stage_child]):
    """
    Enter multi-stage settings menu.
    """

    fluent_name = "multi-stage"

    command_names = \
        ['list_properties']

    _child_classes = dict(
        list_properties=list_properties_cls,
    )

    child_object_type: multi_stage_child = multi_stage_child
    """
    child_object_type of multi_stage.
    """
    return_type = "<object object at 0x7fd93fabcb50>"
