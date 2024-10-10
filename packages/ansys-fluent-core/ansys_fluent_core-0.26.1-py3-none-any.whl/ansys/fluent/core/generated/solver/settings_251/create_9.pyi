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

from .coefficients_2 import coefficients as coefficients_cls
from .distance import distance as distance_cls

class create(CommandWithPositionalArgs):
    fluent_name = ...
    argument_names = ...
    coefficients: coefficients_cls = ...
    distance: distance_cls = ...
