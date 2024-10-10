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

from .cycle_type import cycle_type as cycle_type_cls
from .pseudo_cycle_type import pseudo_cycle_type as pseudo_cycle_type_cls
from .dual_ts_cycle_type import dual_ts_cycle_type as dual_ts_cycle_type_cls

class mg_controls_child(Group):
    fluent_name = ...
    child_names = ...
    cycle_type: cycle_type_cls = ...
    pseudo_cycle_type: pseudo_cycle_type_cls = ...
    dual_ts_cycle_type: dual_ts_cycle_type_cls = ...
