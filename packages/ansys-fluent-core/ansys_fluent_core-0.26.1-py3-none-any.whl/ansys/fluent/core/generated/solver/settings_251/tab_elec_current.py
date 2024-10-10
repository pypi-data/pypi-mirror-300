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

from .option_24 import option as option_cls
from .value_12 import value as value_cls
from .profile_3 import profile as profile_cls

class tab_elec_current(Group):
    """
    Set electric current load at terminal in the CHT-coupling.
    """

    fluent_name = "tab-elec-current"

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

