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

from .delete_1 import delete as delete_cls
from .rename import rename as rename_cls
from .list import list as list_cls
from .list_properties_1 import list_properties as list_properties_cls
from .make_a_copy import make_a_copy as make_a_copy_cls
from .variables_child import variables_child


class qbmm_boundary_value(NamedObject[variables_child], _NonCreatableNamedObjectMixin[variables_child]):
    """
    List of boundary values for QBMM population balance model.
    """

    fluent_name = "qbmm-boundary-value"

    command_names = \
        ['delete', 'rename', 'list', 'list_properties', 'make_a_copy']

    _child_classes = dict(
        delete=delete_cls,
        rename=rename_cls,
        list=list_cls,
        list_properties=list_properties_cls,
        make_a_copy=make_a_copy_cls,
    )

    child_object_type: variables_child = variables_child
    """
    child_object_type of qbmm_boundary_value.
    """
