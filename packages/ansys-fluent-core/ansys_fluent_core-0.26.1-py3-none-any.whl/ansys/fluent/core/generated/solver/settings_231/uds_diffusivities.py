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

from .uds_diffusivities_child import uds_diffusivities_child


class uds_diffusivities(NamedObject[uds_diffusivities_child], _NonCreatableNamedObjectMixin[uds_diffusivities_child]):
    """
    'uds_diffusivities' child.
    """

    fluent_name = "uds-diffusivities"

    child_object_type: uds_diffusivities_child = uds_diffusivities_child
    """
    child_object_type of uds_diffusivities.
    """
    return_type = "<object object at 0x7ff9d1371910>"
