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

from .axis_from import axis_from as axis_from_cls
from .axis_to import axis_to as axis_to_cls

class first_axis(Group):
    """
    'first_axis' child.
    """

    fluent_name = "first-axis"

    child_names = \
        ['axis_from', 'axis_to']

    _child_classes = dict(
        axis_from=axis_from_cls,
        axis_to=axis_to_cls,
    )

    return_type = "<object object at 0x7fe5b915ed30>"
