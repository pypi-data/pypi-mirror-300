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

from .turb_visc_func_mf_child import turb_visc_func_mf_child


class uds_bc(NamedObject[turb_visc_func_mf_child], _NonCreatableNamedObjectMixin[turb_visc_func_mf_child]):
    """
    'uds_bc' child.
    """

    fluent_name = "uds-bc"

    child_object_type: turb_visc_func_mf_child = turb_visc_func_mf_child
    """
    child_object_type of uds_bc.
    """
    return_type = "<object object at 0x7ff9d1559790>"
