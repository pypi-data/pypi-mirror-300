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

from .create_1 import create as create_cls
from .delete_1 import delete as delete_cls
from .rename import rename as rename_cls
from .list_1 import list as list_cls
from .list_properties import list_properties as list_properties_cls
from .make_a_copy import make_a_copy as make_a_copy_cls
from .add import add as add_cls
from .graphics_objects_child import graphics_objects_child


class graphics_objects(NamedObject[graphics_objects_child], CreatableNamedObjectMixin[graphics_objects_child]):
    """
    Enter the graphics objects menu to set Scene parameters.
    """

    fluent_name = "graphics-objects"

    command_names = \
        ['create', 'delete', 'rename', 'list', 'list_properties',
         'make_a_copy', 'add']

    _child_classes = dict(
        create=create_cls,
        delete=delete_cls,
        rename=rename_cls,
        list=list_cls,
        list_properties=list_properties_cls,
        make_a_copy=make_a_copy_cls,
        add=add_cls,
    )

    child_object_type: graphics_objects_child = graphics_objects_child
    """
    child_object_type of graphics_objects.
    """
