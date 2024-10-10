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

from .delete_1 import delete as delete_cls
from .list import list as list_cls
from .list_properties_1 import list_properties as list_properties_cls
from .make_a_copy import make_a_copy as make_a_copy_cls
from .rake_surface_child import rake_surface_child


class rake_surface(NamedObject[rake_surface_child], CreatableNamedObjectMixinOld[rake_surface_child]):
    """
    'rake_surface' child.
    """

    fluent_name = "rake-surface"

    command_names = \
        ['delete', 'list', 'list_properties', 'make_a_copy']

    _child_classes = dict(
        delete=delete_cls,
        list=list_cls,
        list_properties=list_properties_cls,
        make_a_copy=make_a_copy_cls,
    )

    child_object_type: rake_surface_child = rake_surface_child
    """
    child_object_type of rake_surface.
    """
    return_type = "<object object at 0x7fd93f9c1c30>"
