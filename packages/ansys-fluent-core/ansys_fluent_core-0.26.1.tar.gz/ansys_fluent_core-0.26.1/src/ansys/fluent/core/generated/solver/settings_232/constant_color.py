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
from .color import color as color_cls

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

    return_type = "<object object at 0x7fe5b8f47280>"
