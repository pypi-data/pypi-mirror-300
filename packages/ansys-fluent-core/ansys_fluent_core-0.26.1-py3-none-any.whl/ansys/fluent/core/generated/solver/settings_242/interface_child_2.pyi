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

from .name import name as name_cls
from .type_5 import type as type_cls
from .location_2 import location as location_cls
from .phase_38 import phase as phase_cls

class interface_child(Group):
    fluent_name = ...
    child_names = ...
    name: name_cls = ...
    type: type_cls = ...
    location: location_cls = ...
    phase: phase_cls = ...
