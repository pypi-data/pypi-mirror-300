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

from .option_26 import option as option_cls
from .value_15 import value as value_cls

class premix_unburnt_temp(Group):
    """
    Set material property: premix-unburnt-temp.
    """

    fluent_name = "premix-unburnt-temp"

    child_names = \
        ['option', 'value']

    _child_classes = dict(
        option=option_cls,
        value=value_cls,
    )

