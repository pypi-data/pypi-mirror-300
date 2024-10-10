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
from .orthotropic_structure_nu import orthotropic_structure_nu as orthotropic_structure_nu_cls

class struct_poisson_ratio(Group):
    """
    'struct_poisson_ratio' child.
    """

    fluent_name = "struct-poisson-ratio"

    child_names = \
        ['option', 'value', 'orthotropic_structure_nu']

    _child_classes = dict(
        option=option_cls,
        value=value_cls,
        orthotropic_structure_nu=orthotropic_structure_nu_cls,
    )

    return_type = "<object object at 0x7ff9d14fc8b0>"
