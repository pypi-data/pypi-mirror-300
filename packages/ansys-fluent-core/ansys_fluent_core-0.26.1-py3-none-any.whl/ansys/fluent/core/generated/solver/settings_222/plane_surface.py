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

from .plane_surface_child import plane_surface_child


class plane_surface(NamedObject[plane_surface_child], CreatableNamedObjectMixinOld[plane_surface_child]):
    """
    'plane_surface' child.
    """

    fluent_name = "plane-surface"

    child_object_type: plane_surface_child = plane_surface_child
    """
    child_object_type of plane_surface.
    """
    return_type = "<object object at 0x7f82c46613a0>"
