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

from .a_2 import a as a_cls
from .b_1 import b as b_cls
from .c import c as c_cls

class gupta_curve_fit_viscosity(Group):
    fluent_name = ...
    child_names = ...
    a: a_cls = ...
    b: b_cls = ...
    c: c_cls = ...
