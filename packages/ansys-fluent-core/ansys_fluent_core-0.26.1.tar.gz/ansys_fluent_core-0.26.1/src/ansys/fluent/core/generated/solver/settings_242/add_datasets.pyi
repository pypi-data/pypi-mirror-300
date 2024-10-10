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

from .zone_names_7 import zone_names as zone_names_cls
from .domain_2 import domain as domain_cls
from .quantities import quantities as quantities_cls
from .min_2 import min as min_cls
from .max_2 import max as max_cls
from .mean_1 import mean as mean_cls
from .rmse_1 import rmse as rmse_cls
from .moving_average_1 import moving_average as moving_average_cls
from .average_over_2 import average_over as average_over_cls

class add_datasets(Command):
    fluent_name = ...
    argument_names = ...
    zone_names: zone_names_cls = ...
    domain: domain_cls = ...
    quantities: quantities_cls = ...
    min: min_cls = ...
    max: max_cls = ...
    mean: mean_cls = ...
    rmse: rmse_cls = ...
    moving_average: moving_average_cls = ...
    average_over: average_over_cls = ...
