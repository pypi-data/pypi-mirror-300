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
from .aeromechanics_child import aeromechanics_child


class aeromechanics(NamedObject[aeromechanics_child], CreatableNamedObjectMixin[aeromechanics_child]):
    """
    Create a new or edit an existing report definition.
    """

    fluent_name = "aeromechanics"

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

    child_object_type: aeromechanics_child = aeromechanics_child
    """
    child_object_type of aeromechanics.
    """
