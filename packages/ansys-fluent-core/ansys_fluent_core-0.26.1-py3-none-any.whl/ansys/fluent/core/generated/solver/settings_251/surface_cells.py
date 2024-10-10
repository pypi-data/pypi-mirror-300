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
from .surface_cells_child import surface_cells_child


class surface_cells(NamedObject[surface_cells_child], CreatableNamedObjectMixin[surface_cells_child]):
    """
    To extract all cells intersected by a data surface.
    """

    fluent_name = "surface-cells"

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

    child_object_type: surface_cells_child = surface_cells_child
    """
    child_object_type of surface_cells.
    """
