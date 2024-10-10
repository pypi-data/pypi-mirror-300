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

from .number_of_coordinate_intervals import number_of_coordinate_intervals as number_of_coordinate_intervals_cls
from .number_of_velocity_intervals import number_of_velocity_intervals as number_of_velocity_intervals_cls
from .number_of_temperature_intervals import number_of_temperature_intervals as number_of_temperature_intervals_cls

class per_face_parameters(Group):
    fluent_name = ...
    child_names = ...
    number_of_coordinate_intervals: number_of_coordinate_intervals_cls = ...
    number_of_velocity_intervals: number_of_velocity_intervals_cls = ...
    number_of_temperature_intervals: number_of_temperature_intervals_cls = ...
