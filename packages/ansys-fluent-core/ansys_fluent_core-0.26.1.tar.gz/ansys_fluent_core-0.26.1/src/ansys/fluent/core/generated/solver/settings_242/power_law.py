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

from .option_13 import option as option_cls
from .b import b as b_cls
from .reference_viscosity import reference_viscosity as reference_viscosity_cls
from .reference_temperature import reference_temperature as reference_temperature_cls
from .temperature_exponent import temperature_exponent as temperature_exponent_cls

class power_law(Group):
    """
    Power law viscosity settings.
    """

    fluent_name = "power-law"

    child_names = \
        ['option', 'b', 'reference_viscosity', 'reference_temperature',
         'temperature_exponent']

    _child_classes = dict(
        option=option_cls,
        b=b_cls,
        reference_viscosity=reference_viscosity_cls,
        reference_temperature=reference_temperature_cls,
        temperature_exponent=temperature_exponent_cls,
    )

