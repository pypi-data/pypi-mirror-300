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

from .limiter_enabled import limiter_enabled as limiter_enabled_cls
from .report_leidenfrost_temperature import report_leidenfrost_temperature as report_leidenfrost_temperature_cls
from .offset_above_film_boiling_temperature import offset_above_film_boiling_temperature as offset_above_film_boiling_temperature_cls

class wall_film_temperature_limiter(Group):
    fluent_name = ...
    child_names = ...
    limiter_enabled: limiter_enabled_cls = ...
    report_leidenfrost_temperature: report_leidenfrost_temperature_cls = ...
    offset_above_film_boiling_temperature: offset_above_film_boiling_temperature_cls = ...
    return_type = ...
