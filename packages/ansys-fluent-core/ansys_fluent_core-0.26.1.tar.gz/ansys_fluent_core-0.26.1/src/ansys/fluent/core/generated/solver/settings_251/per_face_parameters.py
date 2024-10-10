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

from .number_of_coordinate_intervals import number_of_coordinate_intervals as number_of_coordinate_intervals_cls
from .number_of_velocity_intervals import number_of_velocity_intervals as number_of_velocity_intervals_cls
from .number_of_temperature_intervals import number_of_temperature_intervals as number_of_temperature_intervals_cls

class per_face_parameters(Group):
    """
    Parameters that are used during data evaluation on every face individually.
    """

    fluent_name = "per-face-parameters"

    child_names = \
        ['number_of_coordinate_intervals', 'number_of_velocity_intervals',
         'number_of_temperature_intervals']

    _child_classes = dict(
        number_of_coordinate_intervals=number_of_coordinate_intervals_cls,
        number_of_velocity_intervals=number_of_velocity_intervals_cls,
        number_of_temperature_intervals=number_of_temperature_intervals_cls,
    )

    _child_aliases = dict(
        dpm_data_redu_target_num_pcls_per_face="number_of_coordinate_intervals",
        dpm_data_redu_temperature_intervals="number_of_temperature_intervals",
        dpm_data_redu_velocity_intervals="number_of_velocity_intervals",
    )

