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

from .option_12 import option as option_cls
from .lewis_number import lewis_number as lewis_number_cls
from .value_12 import value as value_cls
from .species_diffusivity import species_diffusivity as species_diffusivity_cls
from .multicomponent import multicomponent as multicomponent_cls
from .user_defined_function import user_defined_function as user_defined_function_cls

class mass_diffusivity(Group):
    """
    Mass-diffusivity property setting for this material.
    """

    fluent_name = "mass-diffusivity"

    child_names = \
        ['option', 'lewis_number', 'value', 'species_diffusivity',
         'multicomponent', 'user_defined_function']

    _child_classes = dict(
        option=option_cls,
        lewis_number=lewis_number_cls,
        value=value_cls,
        species_diffusivity=species_diffusivity_cls,
        multicomponent=multicomponent_cls,
        user_defined_function=user_defined_function_cls,
    )

