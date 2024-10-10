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

from .option_23 import option as option_cls
from .value_11 import value as value_cls
from .profile_2 import profile as profile_cls

class energy_source_active_child(Group):
    """
    'child_object_type' of energy_source_active.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['option', 'value', 'profile']

    _child_classes = dict(
        option=option_cls,
        value=value_cls,
        profile=profile_cls,
    )

    _child_aliases = dict(
        method="option",
    )

