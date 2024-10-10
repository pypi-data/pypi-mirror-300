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

from .name import name as name_cls
from .phase_8 import phase as phase_cls
from .is_not_a_rans_les_interface import is_not_a_rans_les_interface as is_not_a_rans_les_interface_cls

class interior_child(Group):
    """
    'child_object_type' of interior.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'phase', 'is_not_a_rans_les_interface']

    _child_classes = dict(
        name=name_cls,
        phase=phase_cls,
        is_not_a_rans_les_interface=is_not_a_rans_les_interface_cls,
    )

    return_type = "<object object at 0x7fd94d259980>"
