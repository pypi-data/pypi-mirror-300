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
from .reference_frame_velocity_child import reference_frame_velocity_child


class shear_stress(ListObject[reference_frame_velocity_child]):
    """
    'shear_stress' child.
    """

    fluent_name = "shear-stress"

    command_names = \
        ['list_properties']

    _child_classes = dict(
        list_properties=list_properties_cls,
    )

    child_object_type: reference_frame_velocity_child = reference_frame_velocity_child
    """
    child_object_type of shear_stress.
    """
    return_type = "<object object at 0x7fd93fd61fe0>"
