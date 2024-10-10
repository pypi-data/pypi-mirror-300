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

from .function_of import function_of as function_of_cls
from .coefficients import coefficients as coefficients_cls

class polynomial(Group):
    """
    Polynomial settings.
    """

    fluent_name = "polynomial"

    child_names = \
        ['function_of', 'coefficients']

    _child_classes = dict(
        function_of=function_of_cls,
        coefficients=coefficients_cls,
    )

