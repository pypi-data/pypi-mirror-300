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

from .process_count import process_count as process_count_cls
from .host_name import host_name as host_name_cls

class helper_session_setup(Group):
    fluent_name = ...
    child_names = ...
    process_count: process_count_cls = ...
    host_name: host_name_cls = ...
    return_type = ...
