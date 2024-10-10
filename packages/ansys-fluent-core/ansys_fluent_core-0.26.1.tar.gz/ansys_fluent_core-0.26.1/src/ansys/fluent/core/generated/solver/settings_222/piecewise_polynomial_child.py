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

from .minimum import minimum as minimum_cls
from .maximum import maximum as maximum_cls
from .number_of_coeff import number_of_coeff as number_of_coeff_cls
from .coefficients import coefficients as coefficients_cls

class piecewise_polynomial_child(Group):
    """
    'child_object_type' of piecewise_polynomial.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['minimum', 'maximum', 'number_of_coeff', 'coefficients']

    _child_classes = dict(
        minimum=minimum_cls,
        maximum=maximum_cls,
        number_of_coeff=number_of_coeff_cls,
        coefficients=coefficients_cls,
    )

    return_type = "<object object at 0x7f82df9c1440>"
