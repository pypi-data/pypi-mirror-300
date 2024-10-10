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

from .option import option as option_cls
from .smooth import smooth as smooth_cls
from .banded import banded as banded_cls

class coloring(Group):
    """
    'coloring' child.
    """

    fluent_name = "coloring"

    child_names = \
        ['option', 'smooth', 'banded']

    _child_classes = dict(
        option=option_cls,
        smooth=smooth_cls,
        banded=banded_cls,
    )

    return_type = "<object object at 0x7fd93f9c3170>"
