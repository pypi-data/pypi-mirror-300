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

from .convective_heat_transfer import convective_heat_transfer as convective_heat_transfer_cls
from .include_convective_heat_transfer import include_convective_heat_transfer as include_convective_heat_transfer_cls
from .film_movement import film_movement as film_movement_cls
from .lwf_particle_inclusion_in_dpm_concentration_enabled import lwf_particle_inclusion_in_dpm_concentration_enabled as lwf_particle_inclusion_in_dpm_concentration_enabled_cls
from .wall_film_temperature_limiter import wall_film_temperature_limiter as wall_film_temperature_limiter_cls

class wall_film(Group):
    fluent_name = ...
    child_names = ...
    convective_heat_transfer: convective_heat_transfer_cls = ...
    include_convective_heat_transfer: include_convective_heat_transfer_cls = ...
    film_movement: film_movement_cls = ...
    lwf_particle_inclusion_in_dpm_concentration_enabled: lwf_particle_inclusion_in_dpm_concentration_enabled_cls = ...
    wall_film_temperature_limiter: wall_film_temperature_limiter_cls = ...
    return_type = ...
