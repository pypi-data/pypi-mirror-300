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

from .enabled_1 import enabled as enabled_cls
from .ccurv import ccurv as ccurv_cls

class curvature_correction(Group):
    """
    Curvature correction settings.
    """

    fluent_name = "curvature-correction"

    child_names = \
        ['enabled', 'ccurv']

    _child_classes = dict(
        enabled=enabled_cls,
        ccurv=ccurv_cls,
    )

