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

from typing import Union, List, Tuple

from .piecewise_polynomial_child import piecewise_polynomial_child


class piecewise_polynomial(ListObject[piecewise_polynomial_child]):
    fluent_name = ...
    child_object_type: piecewise_polynomial_child = ...
    return_type = ...
