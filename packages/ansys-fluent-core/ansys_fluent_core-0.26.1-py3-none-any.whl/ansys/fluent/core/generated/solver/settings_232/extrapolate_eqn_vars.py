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
from .multi_component_diffusion_mf_child import multi_component_diffusion_mf_child


class extrapolate_eqn_vars(NamedObject[multi_component_diffusion_mf_child], _NonCreatableNamedObjectMixin[multi_component_diffusion_mf_child]):
    """
    Enter the extrapolation menu.
    """

    fluent_name = "extrapolate-eqn-vars"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    _child_classes = dict(
        list=list_cls,
        list_properties=list_properties_cls,
        duplicate=duplicate_cls,
    )

    child_object_type: multi_component_diffusion_mf_child = multi_component_diffusion_mf_child
    """
    child_object_type of extrapolate_eqn_vars.
    """
    return_type = "<object object at 0x7fe5b8f44a20>"
