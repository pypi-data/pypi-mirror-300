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
from .rename import rename as rename_cls
from .list import list as list_cls
from .list_properties_1 import list_properties as list_properties_cls
from .make_a_copy import make_a_copy as make_a_copy_cls
from .imprint_surface_child import imprint_surface_child


class imprint_surface(NamedObject[imprint_surface_child], CreatableNamedObjectMixinOld[imprint_surface_child]):
    """
    Provides access to creating new and editing existing imprint surfaces. You can import a custom surface representing the region of interest (.stl, .msh, or .cas format) and imprint this surface into the current mesh.
    """

    fluent_name = "imprint-surface"

    command_names = \
        ['delete', 'rename', 'list', 'list_properties', 'make_a_copy']

    _child_classes = dict(
        delete=delete_cls,
        rename=rename_cls,
        list=list_cls,
        list_properties=list_properties_cls,
        make_a_copy=make_a_copy_cls,
    )

    child_object_type: imprint_surface_child = imprint_surface_child
    """
    child_object_type of imprint_surface.
    """
