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

from .method_4 import method as method_cls
from .type_1 import type as type_cls
from .frequency_1 import frequency as frequency_cls

class two_session_coupling(Group):
    fluent_name = ...
    child_names = ...
    method: method_cls = ...
    type: type_cls = ...
    frequency: frequency_cls = ...
    return_type = ...
