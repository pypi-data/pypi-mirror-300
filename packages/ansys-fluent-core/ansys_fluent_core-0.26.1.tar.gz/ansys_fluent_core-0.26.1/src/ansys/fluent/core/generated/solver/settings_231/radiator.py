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

from .radiator_child import radiator_child


class radiator(NamedObject[radiator_child], _NonCreatableNamedObjectMixin[radiator_child]):
    """
    'radiator' child.
    """

    fluent_name = "radiator"

    child_object_type: radiator_child = radiator_child
    """
    child_object_type of radiator.
    """
    return_type = "<object object at 0x7ff9d0f86ff0>"
