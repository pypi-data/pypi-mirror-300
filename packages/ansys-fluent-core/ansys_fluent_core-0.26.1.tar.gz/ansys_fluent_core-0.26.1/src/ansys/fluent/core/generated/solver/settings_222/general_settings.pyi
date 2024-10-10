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

from .number_of_iterations import number_of_iterations as number_of_iterations_cls
from .explicit_urf import explicit_urf as explicit_urf_cls
from .reference_frame_1 import reference_frame as reference_frame_cls
from .initial_pressure import initial_pressure as initial_pressure_cls
from .external_aero import external_aero as external_aero_cls
from .const_velocity import const_velocity as const_velocity_cls

class general_settings(Group):
    fluent_name = ...
    child_names = ...
    number_of_iterations: number_of_iterations_cls = ...
    explicit_urf: explicit_urf_cls = ...
    reference_frame: reference_frame_cls = ...
    initial_pressure: initial_pressure_cls = ...
    external_aero: external_aero_cls = ...
    const_velocity: const_velocity_cls = ...
    return_type = ...
