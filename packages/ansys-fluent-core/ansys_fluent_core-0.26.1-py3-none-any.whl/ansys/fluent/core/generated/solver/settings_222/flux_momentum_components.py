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


class flux_momentum_components(ListObject[child_object_type_child]):
    """
    'flux_momentum_components' child.
    """

    fluent_name = "flux-momentum-components"

    child_object_type: child_object_type_child = child_object_type_child
    """
    child_object_type of flux_momentum_components.
    """
    return_type = "<object object at 0x7f82c5a97a80>"
