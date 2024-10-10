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

from .minimum_6 import minimum as minimum_cls
from .maximum_5 import maximum as maximum_cls
from .compute_8 import compute as compute_cls

class range(Group):
    """
    Specifies Range for Filter Settings.
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

