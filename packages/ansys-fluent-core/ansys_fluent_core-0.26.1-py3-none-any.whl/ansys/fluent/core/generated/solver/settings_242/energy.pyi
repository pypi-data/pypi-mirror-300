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

from .enabled import enabled as enabled_cls
from .viscous_dissipation import viscous_dissipation as viscous_dissipation_cls
from .pressure_work import pressure_work as pressure_work_cls
from .kinetic_energy import kinetic_energy as kinetic_energy_cls
from .inlet_diffusion import inlet_diffusion as inlet_diffusion_cls
from .two_temperature import two_temperature as two_temperature_cls

class energy(Group):
    fluent_name = ...
    child_names = ...
    enabled: enabled_cls = ...
    viscous_dissipation: viscous_dissipation_cls = ...
    pressure_work: pressure_work_cls = ...
    kinetic_energy: kinetic_energy_cls = ...
    inlet_diffusion: inlet_diffusion_cls = ...
    two_temperature: two_temperature_cls = ...
