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

from .x_axis_4 import x_axis as x_axis_cls
from .y_axis_4 import y_axis as y_axis_cls

class labels(Group):
    """
    'labels' child.
    """

    fluent_name = "labels"

    child_names = \
        ['x_axis', 'y_axis']

    _child_classes = dict(
        x_axis=x_axis_cls,
        y_axis=y_axis_cls,
    )

    return_type = "<object object at 0x7fd93f8cc1d0>"
