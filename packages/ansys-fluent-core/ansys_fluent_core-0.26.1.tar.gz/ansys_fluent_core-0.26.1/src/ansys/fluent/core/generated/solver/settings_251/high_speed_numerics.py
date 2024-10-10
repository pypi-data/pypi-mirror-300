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

from .enable_23 import enable as enable_cls
from .expert_7 import expert as expert_cls
from .visualize_pressure_discontinuity_sensor import visualize_pressure_discontinuity_sensor as visualize_pressure_discontinuity_sensor_cls

class high_speed_numerics(Group):
    """
    Enter high-speed-numerics menu.
    """

    fluent_name = "high-speed-numerics"

    child_names = \
        ['enable', 'expert', 'visualize_pressure_discontinuity_sensor']

    _child_classes = dict(
        enable=enable_cls,
        expert=expert_cls,
        visualize_pressure_discontinuity_sensor=visualize_pressure_discontinuity_sensor_cls,
    )

