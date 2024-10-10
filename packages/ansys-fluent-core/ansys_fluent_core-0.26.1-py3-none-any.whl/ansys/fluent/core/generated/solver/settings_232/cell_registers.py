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
from .cell_registers_child import cell_registers_child


class cell_registers(NamedObject[cell_registers_child], CreatableNamedObjectMixinOld[cell_registers_child]):
    """
    'cell_registers' child.
    """

    fluent_name = "cell-registers"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    _child_classes = dict(
        list=list_cls,
        list_properties=list_properties_cls,
        duplicate=duplicate_cls,
    )

    child_object_type: cell_registers_child = cell_registers_child
    """
    child_object_type of cell_registers.
    """
    return_type = "<object object at 0x7fe5b905ad70>"
