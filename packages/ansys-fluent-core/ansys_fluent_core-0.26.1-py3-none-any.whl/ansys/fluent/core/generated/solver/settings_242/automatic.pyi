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

from .option_1 import option as option_cls
from .type_10 import type as type_cls
from .id import id as id_cls
from .normal_1 import normal as normal_cls
from .partition import partition as partition_cls

class automatic(Group):
    fluent_name = ...
    child_names = ...
    option: option_cls = ...
    type: type_cls = ...
    id: id_cls = ...
    normal: normal_cls = ...
    partition: partition_cls = ...
