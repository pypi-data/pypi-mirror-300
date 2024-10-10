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

from .auto_range_1 import auto_range as auto_range_cls
from .minimum_3 import minimum as minimum_cls
from .maximum_3 import maximum as maximum_cls
from .compute_5 import compute as compute_cls

class range_options(Group):
    """
    Choose min max of the range.
    """

    fluent_name = "range-options"

    child_names = \
        ['auto_range', 'minimum', 'maximum']

    command_names = \
        ['compute']

    _child_classes = dict(
        auto_range=auto_range_cls,
        minimum=minimum_cls,
        maximum=maximum_cls,
        compute=compute_cls,
    )

