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
from .resize import resize as resize_cls
from .add_zone import add_zone as add_zone_cls
from .list_zone import list_zone as list_zone_cls
from .delete_zone import delete_zone as delete_zone_cls
from .contact_resis_child import contact_resis_child


class tortuosity_interface(ListObject[contact_resis_child]):
    """
    Setup tortuosity zones and values.
    """

    fluent_name = "tortuosity-interface"

    command_names = \
        ['list_properties', 'resize', 'add_zone', 'list_zone', 'delete_zone']

    _child_classes = dict(
        list_properties=list_properties_cls,
        resize=resize_cls,
        add_zone=add_zone_cls,
        list_zone=list_zone_cls,
        delete_zone=delete_zone_cls,
    )

    child_object_type: contact_resis_child = contact_resis_child
    """
    child_object_type of tortuosity_interface.
    """
