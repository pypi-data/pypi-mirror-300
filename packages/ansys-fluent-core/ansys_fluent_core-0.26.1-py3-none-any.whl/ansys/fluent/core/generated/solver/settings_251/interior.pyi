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

from .is_not_a_rans_les_interface import is_not_a_rans_les_interface as is_not_a_rans_les_interface_cls

class interior(Group):
    fluent_name = ...
    child_names = ...
    is_not_a_rans_les_interface: is_not_a_rans_les_interface_cls = ...
