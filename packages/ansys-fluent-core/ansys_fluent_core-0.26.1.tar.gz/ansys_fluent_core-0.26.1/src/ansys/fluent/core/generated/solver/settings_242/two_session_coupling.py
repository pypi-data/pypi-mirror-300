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

from .method_23 import method as method_cls
from .type_2 import type as type_cls
from .frequency_9 import frequency as frequency_cls

class two_session_coupling(Group):
    """
    'two_session_coupling' child.
    """

    fluent_name = "two-session-coupling"

    child_names = \
        ['method', 'type', 'frequency']

    _child_classes = dict(
        method=method_cls,
        type=type_cls,
        frequency=frequency_cls,
    )

