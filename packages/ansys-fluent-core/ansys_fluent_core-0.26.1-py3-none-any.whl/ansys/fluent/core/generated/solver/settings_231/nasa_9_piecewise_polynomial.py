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

from .piecewise_polynomial_child import piecewise_polynomial_child


class nasa_9_piecewise_polynomial(ListObject[piecewise_polynomial_child]):
    """
    'nasa_9_piecewise_polynomial' child.
    """

    fluent_name = "nasa-9-piecewise-polynomial"

    child_object_type: piecewise_polynomial_child = piecewise_polynomial_child
    """
    child_object_type of nasa_9_piecewise_polynomial.
    """
    return_type = "<object object at 0x7ff9d1370ab0>"
