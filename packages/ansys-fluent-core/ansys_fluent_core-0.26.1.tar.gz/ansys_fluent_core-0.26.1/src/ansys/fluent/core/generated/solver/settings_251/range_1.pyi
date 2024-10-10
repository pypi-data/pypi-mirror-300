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

from .minimum_1 import minimum as minimum_cls
from .maximum_1 import maximum as maximum_cls
from .compute_3 import compute as compute_cls

class range(Group):
    fluent_name = ...
    child_names = ...
    minimum: minimum_cls = ...
    maximum: maximum_cls = ...
    command_names = ...

    def compute(self, ):
        """
        Sets the 'minimum' and 'maximum' fields based on the current solution data.
        """

