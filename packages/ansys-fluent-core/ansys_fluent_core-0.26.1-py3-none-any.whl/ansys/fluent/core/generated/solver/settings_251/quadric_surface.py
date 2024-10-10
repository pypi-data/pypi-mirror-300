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
from .list import list as list_cls
from .list_properties import list_properties as list_properties_cls
from .make_a_copy import make_a_copy as make_a_copy_cls
from .quadric_surface_child import quadric_surface_child


class quadric_surface(NamedObject[quadric_surface_child], CreatableNamedObjectMixin[quadric_surface_child]):
    """
    Provides access to creating new and editing existing quadric surfaces. You can display data on a general quadric surface where you can specify the surface by entering the coefficients of the quadric function that defines it. This feature provides you with an explicit method for defining surfaces.
    """

    fluent_name = "quadric-surface"

    command_names = \
        ['create', 'delete', 'rename', 'list', 'list_properties',
         'make_a_copy']

    _child_classes = dict(
        create=create_cls,
        delete=delete_cls,
        rename=rename_cls,
        list=list_cls,
        list_properties=list_properties_cls,
        make_a_copy=make_a_copy_cls,
    )

    child_object_type: quadric_surface_child = quadric_surface_child
    """
    child_object_type of quadric_surface.
    """
