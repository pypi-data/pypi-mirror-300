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

from .list import list as list_cls
from .list_properties import list_properties as list_properties_cls
from .duplicate import duplicate as duplicate_cls
from .display_2 import display as display_cls
from .copy_4 import copy as copy_cls
from .add_to_graphics import add_to_graphics as add_to_graphics_cls
from .clear_history import clear_history as clear_history_cls
from .scene_child import scene_child


class scene(NamedObject[scene_child], CreatableNamedObjectMixinOld[scene_child]):
    """
    'scene' child.
    """

    fluent_name = "scene"

    command_names = \
        ['list', 'list_properties', 'duplicate', 'display', 'copy',
         'add_to_graphics', 'clear_history']

    _child_classes = dict(
        list=list_cls,
        list_properties=list_properties_cls,
        duplicate=duplicate_cls,
        display=display_cls,
        copy=copy_cls,
        add_to_graphics=add_to_graphics_cls,
        clear_history=clear_history_cls,
    )

    child_object_type: scene_child = scene_child
    """
    child_object_type of scene.
    """
    return_type = "<object object at 0x7fe5b8e2dd70>"
