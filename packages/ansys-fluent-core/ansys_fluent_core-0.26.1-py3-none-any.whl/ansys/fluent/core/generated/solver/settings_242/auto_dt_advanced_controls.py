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

from .enable_17 import enable as enable_cls
from .dt_init_limit import dt_init_limit as dt_init_limit_cls
from .dt_max_1 import dt_max as dt_max_cls
from .dt_factor_min import dt_factor_min as dt_factor_min_cls
from .dt_factor_max import dt_factor_max as dt_factor_max_cls
from .max_velocity_ratio import max_velocity_ratio as max_velocity_ratio_cls

class auto_dt_advanced_controls(Group):
    """
    Set automatic time-stepping controls for better solution stability.
    """

    fluent_name = "auto-dt-advanced-controls"

    child_names = \
        ['enable', 'dt_init_limit', 'dt_max', 'dt_factor_min',
         'dt_factor_max', 'max_velocity_ratio']

    _child_classes = dict(
        enable=enable_cls,
        dt_init_limit=dt_init_limit_cls,
        dt_max=dt_max_cls,
        dt_factor_min=dt_factor_min_cls,
        dt_factor_max=dt_factor_max_cls,
        max_velocity_ratio=max_velocity_ratio_cls,
    )

