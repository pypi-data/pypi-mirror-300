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

from .x_5 import x as x_cls
from .y_5 import y as y_cls
from .background_color import background_color as background_color_cls

class axes(Group):
    """
    Axes-properties.
    """

    fluent_name = "axes"

    child_names = \
        ['x', 'y', 'background_color']

    _child_classes = dict(
        x=x_cls,
        y=y_cls,
        background_color=background_color_cls,
    )

