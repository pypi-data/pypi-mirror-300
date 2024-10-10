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

from .list_properties_1 import list_properties as list_properties_cls
from .piecewise_linear_child import piecewise_linear_child


class piecewise_linear(ListObject[piecewise_linear_child]):
    """
    'piecewise_linear' child.
    """

    fluent_name = "piecewise-linear"

    command_names = \
        ['list_properties']

    _child_classes = dict(
        list_properties=list_properties_cls,
    )

    child_object_type: piecewise_linear_child = piecewise_linear_child
    """
    child_object_type of piecewise_linear.
    """
    return_type = "<object object at 0x7fe5bb5017c0>"
