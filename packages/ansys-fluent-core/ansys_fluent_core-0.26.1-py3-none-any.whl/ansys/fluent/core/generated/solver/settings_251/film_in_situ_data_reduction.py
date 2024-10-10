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

from .enabled_42 import enabled as enabled_cls
from .time_of_first_execution import time_of_first_execution as time_of_first_execution_cls
from .execution_time_interval import execution_time_interval as execution_time_interval_cls
from .per_face_parameters import per_face_parameters as per_face_parameters_cls

class film_in_situ_data_reduction(Group):
    """
    Enable and configure the feature that reduces the film particle (parcel) count by combining parcels with similar properties into one.
    """

    fluent_name = "film-in-situ-data-reduction"

    child_names = \
        ['enabled', 'time_of_first_execution', 'execution_time_interval',
         'per_face_parameters']

    _child_classes = dict(
        enabled=enabled_cls,
        time_of_first_execution=time_of_first_execution_cls,
        execution_time_interval=execution_time_interval_cls,
        per_face_parameters=per_face_parameters_cls,
    )

    _child_aliases = dict(
        additional_temperature_intervals="per_face_parameters/number_of_temperature_intervals",
        additional_velocity_intervals="per_face_parameters/number_of_velocity_intervals",
        data_reduction_time_first_execution="time_of_first_execution",
        data_reduction_time_interval="execution_time_interval",
        dpm_in_situ_data_reduction="enabled",
        target_num_parcels_per_face="per_face_parameters/number_of_coordinate_intervals",
    )

