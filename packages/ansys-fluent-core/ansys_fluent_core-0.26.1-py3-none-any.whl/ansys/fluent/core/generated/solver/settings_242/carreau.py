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

from .option_14 import option as option_cls
from .time_constant_1 import time_constant as time_constant_cls
from .power_law_index import power_law_index as power_law_index_cls
from .zero_shear_viscosity import zero_shear_viscosity as zero_shear_viscosity_cls
from .infinite_shear_viscosity import infinite_shear_viscosity as infinite_shear_viscosity_cls
from .reference_temperature import reference_temperature as reference_temperature_cls
from .activation_energy import activation_energy as activation_energy_cls

class carreau(Group):
    """
    Carreau viscosity settings.
    """

    fluent_name = "carreau"

    child_names = \
        ['option', 'time_constant', 'power_law_index', 'zero_shear_viscosity',
         'infinite_shear_viscosity', 'reference_temperature',
         'activation_energy']

    _child_classes = dict(
        option=option_cls,
        time_constant=time_constant_cls,
        power_law_index=power_law_index_cls,
        zero_shear_viscosity=zero_shear_viscosity_cls,
        infinite_shear_viscosity=infinite_shear_viscosity_cls,
        reference_temperature=reference_temperature_cls,
        activation_energy=activation_energy_cls,
    )

