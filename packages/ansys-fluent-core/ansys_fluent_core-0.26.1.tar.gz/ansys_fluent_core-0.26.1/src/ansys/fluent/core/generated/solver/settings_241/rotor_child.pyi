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
from .general_1 import general as general_cls
from .geometry_1 import geometry as geometry_cls
from .trimming import trimming as trimming_cls

class rotor_child(Group):
    fluent_name = ...
    child_names = ...
    name: name_cls = ...
    general: general_cls = ...
    geometry: geometry_cls = ...
    trimming: trimming_cls = ...
    return_type = ...
