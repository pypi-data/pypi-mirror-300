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

from .list_properties import list_properties as list_properties_cls
from .piecewise_polynomial_child import piecewise_polynomial_child


class piecewise_polynomial(ListObject[piecewise_polynomial_child]):
    """
    Specify piecewise-polynomial settings.
    """

    fluent_name = "piecewise-polynomial"

    command_names = \
        ['list_properties']

    _child_classes = dict(
        list_properties=list_properties_cls,
    )

    child_object_type: piecewise_polynomial_child = piecewise_polynomial_child
    """
    child_object_type of piecewise_polynomial.
    """
    return_type = "<object object at 0x7fd94caba2f0>"
