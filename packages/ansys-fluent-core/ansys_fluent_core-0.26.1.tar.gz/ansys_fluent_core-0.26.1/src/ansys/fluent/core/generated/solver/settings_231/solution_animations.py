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

from .display_1 import display as display_cls
from .copy_3 import copy as copy_cls
from .add_to_graphics import add_to_graphics as add_to_graphics_cls
from .clear_history import clear_history as clear_history_cls
from .solution_animations_child import solution_animations_child


class solution_animations(NamedObject[solution_animations_child], CreatableNamedObjectMixinOld[solution_animations_child]):
    """
    'solution_animations' child.
    """

    fluent_name = "solution-animations"

    command_names = \
        ['display', 'copy', 'add_to_graphics', 'clear_history']

    _child_classes = dict(
        display=display_cls,
        copy=copy_cls,
        add_to_graphics=add_to_graphics_cls,
        clear_history=clear_history_cls,
    )

    child_object_type: solution_animations_child = solution_animations_child
    """
    child_object_type of solution_animations.
    """
    return_type = "<object object at 0x7ff9d0a625c0>"
