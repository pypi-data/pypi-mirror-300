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

from .minimum_1 import minimum as minimum_cls
from .maximum_1 import maximum as maximum_cls
from .compute_3 import compute as compute_cls

class range(Group):
    """
    Indicates minimum and maximum values of the selected field variable in the selected surfaces and/or cell zones.
    """

    fluent_name = "range"

    child_names = \
        ['minimum', 'maximum']

    command_names = \
        ['compute']

    _child_classes = dict(
        minimum=minimum_cls,
        maximum=maximum_cls,
        compute=compute_cls,
    )

