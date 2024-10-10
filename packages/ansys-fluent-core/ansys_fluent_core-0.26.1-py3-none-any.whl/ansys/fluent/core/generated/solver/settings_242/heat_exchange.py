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

from .option_1 import option as option_cls
from .const_htc import const_htc as const_htc_cls
from .const_nu import const_nu as const_nu_cls

class heat_exchange(Group):
    """
    'heat_exchange' child.
    """

    fluent_name = "heat-exchange"

    child_names = \
        ['option', 'const_htc', 'const_nu']

    _child_classes = dict(
        option=option_cls,
        const_htc=const_htc_cls,
        const_nu=const_nu_cls,
    )

