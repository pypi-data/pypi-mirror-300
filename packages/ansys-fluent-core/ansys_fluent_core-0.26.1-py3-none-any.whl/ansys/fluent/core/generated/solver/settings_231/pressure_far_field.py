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

from .pressure_far_field_child import pressure_far_field_child


class pressure_far_field(NamedObject[pressure_far_field_child], _NonCreatableNamedObjectMixin[pressure_far_field_child]):
    """
    'pressure_far_field' child.
    """

    fluent_name = "pressure-far-field"

    child_object_type: pressure_far_field_child = pressure_far_field_child
    """
    child_object_type of pressure_far_field.
    """
    return_type = "<object object at 0x7ff9d1d70040>"
