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

from .auto_scale import auto_scale as auto_scale_cls
from .scale_f import scale_f as scale_f_cls

class scale(Group):
    """
    Select a number by which the vector size would be scaled.
    """

    fluent_name = "scale"

    child_names = \
        ['auto_scale', 'scale_f']

    _child_classes = dict(
        auto_scale=auto_scale_cls,
        scale_f=scale_f_cls,
    )

