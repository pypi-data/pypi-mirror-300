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

from .is_not_a_rans_les_interface import is_not_a_rans_les_interface as is_not_a_rans_les_interface_cls

class interior(Group):
    """
    Help not available.
    """

    fluent_name = "interior"

    child_names = \
        ['is_not_a_rans_les_interface']

    _child_classes = dict(
        is_not_a_rans_les_interface=is_not_a_rans_les_interface_cls,
    )

