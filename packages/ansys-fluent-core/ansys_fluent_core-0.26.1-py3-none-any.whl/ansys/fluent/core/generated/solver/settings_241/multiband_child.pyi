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
from .start_1 import start as start_cls
from .end import end as end_cls

class multiband_child(Group):
    fluent_name = ...
    child_names = ...
    name: name_cls = ...
    start: start_cls = ...
    end: end_cls = ...
    return_type = ...
