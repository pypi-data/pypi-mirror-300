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


class discretization_scheme(NamedObject[turb_visc_func_mf_child], _NonCreatableNamedObjectMixin[turb_visc_func_mf_child]):
    """
    'discretization_scheme' child.
    """

    fluent_name = "discretization-scheme"

    child_object_type: turb_visc_func_mf_child = turb_visc_func_mf_child
    """
    child_object_type of discretization_scheme.
    """
    return_type = "<object object at 0x7ff9d0b7b940>"
