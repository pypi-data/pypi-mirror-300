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

from .use import use as use_cls
from .user_defined_6 import user_defined as user_defined_cls
from .value_1 import value as value_cls

class isat_weight(Group):
    """
    Set ISAT weight.
    """

    fluent_name = "isat-weight"

    child_names = \
        ['use', 'user_defined', 'value']

    _child_classes = dict(
        use=use_cls,
        user_defined=user_defined_cls,
        value=value_cls,
    )

    return_type = "<object object at 0x7fd93f6c47a0>"
