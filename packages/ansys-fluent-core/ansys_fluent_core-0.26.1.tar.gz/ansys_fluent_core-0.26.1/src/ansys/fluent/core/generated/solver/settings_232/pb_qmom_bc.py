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
from .turb_visc_func_mf_child import turb_visc_func_mf_child


class pb_qmom_bc(NamedObject[turb_visc_func_mf_child], _NonCreatableNamedObjectMixin[turb_visc_func_mf_child]):
    """
    'pb_qmom_bc' child.
    """

    fluent_name = "pb-qmom-bc"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    _child_classes = dict(
        list=list_cls,
        list_properties=list_properties_cls,
        duplicate=duplicate_cls,
    )

    child_object_type: turb_visc_func_mf_child = turb_visc_func_mf_child
    """
    child_object_type of pb_qmom_bc.
    """
    return_type = "<object object at 0x7fe5ba9ebe30>"
