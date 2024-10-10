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

from .minimum_5 import minimum as minimum_cls
from .maximun import maximun as maximun_cls
from .compute_7 import compute as compute_cls

class range_ribbon(Group):
    fluent_name = ...
    child_names = ...
    minimum: minimum_cls = ...
    maximun: maximun_cls = ...
    command_names = ...

    def compute(self, ):
        """
        Update min-max for Twist Range for Ribbon Style.
        """

