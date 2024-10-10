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

from .exponent_h2 import exponent_h2 as exponent_h2_cls
from .exponent_o2 import exponent_o2 as exponent_o2_cls
from .exponent_h2o import exponent_h2o as exponent_h2o_cls

class concentration_exp(Group):
    fluent_name = ...
    child_names = ...
    exponent_h2: exponent_h2_cls = ...
    exponent_o2: exponent_o2_cls = ...
    exponent_h2o: exponent_h2o_cls = ...
