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

from .enabled_30 import enabled as enabled_cls
from .value_10 import value as value_cls

class joule_heat_parameter(Group):
    """
    Set joule heat parameter related settings in ROM.
    """

    fluent_name = "joule-heat-parameter"

    child_names = \
        ['enabled', 'value']

    _child_classes = dict(
        enabled=enabled_cls,
        value=value_cls,
    )

