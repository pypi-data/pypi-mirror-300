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

from .acd import acd as acd_cls
from .cd import cd as cd_cls
from .direction_2 import direction as direction_cls
from .angle_1 import angle as angle_cls

class dynamic_injection_child(Group):
    fluent_name = ...
    child_names = ...
    acd: acd_cls = ...
    cd: cd_cls = ...
    direction: direction_cls = ...
    angle: angle_cls = ...
    return_type = ...
