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
from .color_3 import color as color_cls

class constant_color(Group):
    """
    'constant_color' child.
    """

    fluent_name = "constant-color"

    child_names = \
        ['enabled', 'color']

    _child_classes = dict(
        enabled=enabled_cls,
        color=color_cls,
    )

