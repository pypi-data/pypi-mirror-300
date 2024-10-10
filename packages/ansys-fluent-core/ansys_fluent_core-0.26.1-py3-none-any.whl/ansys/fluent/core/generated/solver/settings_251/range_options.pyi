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

from .global_range_1 import global_range as global_range_cls
from .auto_range_1 import auto_range as auto_range_cls
from .clip_to_range_1 import clip_to_range as clip_to_range_cls
from .minimum_3 import minimum as minimum_cls
from .maximum_3 import maximum as maximum_cls
from .compute_5 import compute as compute_cls

class range_options(Group):
    fluent_name = ...
    child_names = ...
    global_range: global_range_cls = ...
    auto_range: auto_range_cls = ...
    clip_to_range: clip_to_range_cls = ...
    minimum: minimum_cls = ...
    maximum: maximum_cls = ...
    command_names = ...

    def compute(self, ):
        """
        Update min-max for Range object.
        """

