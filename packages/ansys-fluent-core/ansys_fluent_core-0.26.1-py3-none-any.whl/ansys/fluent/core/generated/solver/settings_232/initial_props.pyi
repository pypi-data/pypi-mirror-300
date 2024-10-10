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

from .location_1 import location as location_cls
from .matrix import matrix as matrix_cls
from .cone_settings import cone_settings as cone_settings_cls
from .velocity import velocity as velocity_cls
from .angular_velocity import angular_velocity as angular_velocity_cls
from .mass_flow_rate import mass_flow_rate as mass_flow_rate_cls
from .times import times as times_cls
from .particle_size import particle_size as particle_size_cls
from .temperature import temperature as temperature_cls
from .temperature_2 import temperature_2 as temperature_2_cls

class initial_props(Group):
    fluent_name = ...
    child_names = ...
    location: location_cls = ...
    matrix: matrix_cls = ...
    cone_settings: cone_settings_cls = ...
    velocity: velocity_cls = ...
    angular_velocity: angular_velocity_cls = ...
    mass_flow_rate: mass_flow_rate_cls = ...
    times: times_cls = ...
    particle_size: particle_size_cls = ...
    temperature: temperature_cls = ...
    temperature_2: temperature_2_cls = ...
    return_type = ...
