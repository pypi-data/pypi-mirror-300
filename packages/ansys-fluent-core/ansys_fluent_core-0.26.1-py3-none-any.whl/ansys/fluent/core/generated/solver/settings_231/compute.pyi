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

from .from_zone_type import from_zone_type as from_zone_type_cls
from .from_zone_name import from_zone_name as from_zone_name_cls
from .phase_25 import phase as phase_cls

class compute(Command):
    fluent_name = ...
    argument_names = ...
    from_zone_type: from_zone_type_cls = ...
    from_zone_name: from_zone_name_cls = ...
    phase: phase_cls = ...
    return_type = ...
