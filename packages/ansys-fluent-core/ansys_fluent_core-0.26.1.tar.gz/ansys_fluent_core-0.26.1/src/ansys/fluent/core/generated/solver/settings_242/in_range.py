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

from .value1 import value1 as value1_cls
from .value2 import value2 as value2_cls

class in_range(Group):
    """
    'in_range' child.
    """

    fluent_name = "in-range"

    child_names = \
        ['value1', 'value2']

    _child_classes = dict(
        value1=value1_cls,
        value2=value2_cls,
    )

