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

from .iter_per_coupling_count import iter_per_coupling_count as iter_per_coupling_count_cls
from .single_session_coupling import single_session_coupling as single_session_coupling_cls
from .two_session_coupling import two_session_coupling as two_session_coupling_cls

class coupling(Group):
    fluent_name = ...
    child_names = ...
    iter_per_coupling_count: iter_per_coupling_count_cls = ...
    single_session_coupling: single_session_coupling_cls = ...
    two_session_coupling: two_session_coupling_cls = ...
    return_type = ...
