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

from .display import display as display_cls
from .pathlines_child import pathlines_child


class pathlines(NamedObject[pathlines_child], CreatableNamedObjectMixinOld[pathlines_child]):
    """
    'pathlines' child.
    """

    fluent_name = "pathlines"

    command_names = \
        ['display']

    _child_classes = dict(
        display=display_cls,
    )

    child_object_type: pathlines_child = pathlines_child
    """
    child_object_type of pathlines.
    """
    return_type = "<object object at 0x7f82c5863c50>"
