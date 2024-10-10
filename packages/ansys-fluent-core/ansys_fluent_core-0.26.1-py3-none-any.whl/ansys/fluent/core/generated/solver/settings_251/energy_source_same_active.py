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

from .option_22 import option as option_cls
from .value_10 import value as value_cls
from .profile_1 import profile as profile_cls

class energy_source_same_active(Group):
    """
    Set same energy source for all zones.
    """

    fluent_name = "energy-source-same-active"

    child_names = \
        ['option', 'value', 'profile']

    _child_classes = dict(
        option=option_cls,
        value=value_cls,
        profile=profile_cls,
    )

    _child_aliases = dict(
        data_type="option",
    )

