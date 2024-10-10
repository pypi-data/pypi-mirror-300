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

from .graphics import graphics as graphics_cls
from .surfaces_1 import surfaces as surfaces_cls

class results(Group):
    """
    'results' child.
    """

    fluent_name = "results"

    child_names = \
        ['graphics', 'surfaces']

    _child_classes = dict(
        graphics=graphics_cls,
        surfaces=surfaces_cls,
    )

    return_type = "<object object at 0x7f82c4661510>"
