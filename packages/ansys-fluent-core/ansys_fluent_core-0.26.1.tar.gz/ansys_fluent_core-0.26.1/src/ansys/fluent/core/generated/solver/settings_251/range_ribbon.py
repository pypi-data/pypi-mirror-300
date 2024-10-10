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

from .minimum_5 import minimum as minimum_cls
from .maximun import maximun as maximun_cls
from .compute_7 import compute as compute_cls

class range_ribbon(Group):
    """
    Specifies Range for Ribbon Style.
    """

    fluent_name = "range-ribbon"

    child_names = \
        ['minimum', 'maximun']

    command_names = \
        ['compute']

    _child_classes = dict(
        minimum=minimum_cls,
        maximun=maximun_cls,
        compute=compute_cls,
    )

