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

from .color import color as color_cls
from .weight import weight as weight_cls

class major_gridlines(Group):
    """
    Set properties of gridlines on axis.
    """

    fluent_name = "major-gridlines"

    child_names = \
        ['color', 'weight']

    _child_classes = dict(
        color=color_cls,
        weight=weight_cls,
    )

