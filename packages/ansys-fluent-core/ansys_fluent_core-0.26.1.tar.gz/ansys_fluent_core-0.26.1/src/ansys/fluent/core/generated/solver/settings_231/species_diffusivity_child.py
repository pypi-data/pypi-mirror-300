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

from .option_10 import option as option_cls
from .value import value as value_cls
from .polynomial import polynomial as polynomial_cls

class species_diffusivity_child(Group):
    """
    'child_object_type' of species_diffusivity.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['option', 'value', 'polynomial']

    _child_classes = dict(
        option=option_cls,
        value=value_cls,
        polynomial=polynomial_cls,
    )

    return_type = "<object object at 0x7ff9d14fd7b0>"
