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


class band_q_irrad(NamedObject[child_object_type_child], CreatableNamedObjectMixinOld[child_object_type_child]):
    """
    'band_q_irrad' child.
    """

    fluent_name = "band-q-irrad"

    child_object_type: child_object_type_child = child_object_type_child
    """
    child_object_type of band_q_irrad.
    """
    return_type = "<object object at 0x7f82c69e8080>"
