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

from .child_object_type_child import child_object_type_child


class band_in_emiss(NamedObject[child_object_type_child], CreatableNamedObjectMixinOld[child_object_type_child]):
    """
    'band_in_emiss' child.
    """

    fluent_name = "band-in-emiss"

    child_object_type: child_object_type_child = child_object_type_child
    """
    child_object_type of band_in_emiss.
    """
    return_type = "<object object at 0x7f82c5a95f50>"
