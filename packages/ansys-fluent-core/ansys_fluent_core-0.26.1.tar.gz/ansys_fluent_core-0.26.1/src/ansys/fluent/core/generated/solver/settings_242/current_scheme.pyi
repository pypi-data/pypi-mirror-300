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

from .method_12 import method as method_cls
from .dissipation import dissipation as dissipation_cls
from .residual_minimization import residual_minimization as residual_minimization_cls

class current_scheme(Group):
    fluent_name = ...
    child_names = ...
    method: method_cls = ...
    dissipation: dissipation_cls = ...
    residual_minimization: residual_minimization_cls = ...
