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

from .polar_pair_list_child import polar_pair_list_child


class polar_pair_list(ListObject[polar_pair_list_child]):
    """
    'polar_pair_list' child.
    """

    fluent_name = "polar-pair-list"

    child_object_type: polar_pair_list_child = polar_pair_list_child
    """
    child_object_type of polar_pair_list.
    """
    return_type = "<object object at 0x7f82c5a95fd0>"
