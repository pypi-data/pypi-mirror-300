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

from .phase_8 import phase as phase_cls
from .name_2 import name as name_cls
from .is_not_a_rans_les_interface import is_not_a_rans_les_interface as is_not_a_rans_les_interface_cls

class interior_child(Group):
    fluent_name = ...
    child_names = ...
    phase: phase_cls = ...
    name: name_cls = ...
    is_not_a_rans_les_interface: is_not_a_rans_les_interface_cls = ...
    return_type = ...
