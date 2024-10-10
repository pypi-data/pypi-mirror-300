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

from .enabled_45 import enabled as enabled_cls
from .set_2 import set as set_cls

class laplace_smoothing(Group):
    """
    'laplace_smoothing' child.
    """

    fluent_name = "laplace-smoothing"

    child_names = \
        ['enabled', 'set']

    _child_classes = dict(
        enabled=enabled_cls,
        set=set_cls,
    )

