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

from .enabled_2 import enabled as enabled_cls
from .ccorner import ccorner as ccorner_cls

class corner_flow_correction(Group):
    """
    Corner flow correction settings.
    """

    fluent_name = "corner-flow-correction"

    child_names = \
        ['enabled', 'ccorner']

    _child_classes = dict(
        enabled=enabled_cls,
        ccorner=ccorner_cls,
    )

