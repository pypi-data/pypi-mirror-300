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

from .type_2 import type as type_cls
from .minimum_1 import minimum as minimum_cls
from .maximum_1 import maximum as maximum_cls

class range_options(Group):
    fluent_name = ...
    child_names = ...
    type: type_cls = ...
    minimum: minimum_cls = ...
    maximum: maximum_cls = ...
    return_type = ...
