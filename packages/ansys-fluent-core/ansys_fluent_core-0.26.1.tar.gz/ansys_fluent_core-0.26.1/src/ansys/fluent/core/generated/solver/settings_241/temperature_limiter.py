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

from .leidenfrost_temp_postproc_enabled import leidenfrost_temp_postproc_enabled as leidenfrost_temp_postproc_enabled_cls
from .enabled_10 import enabled as enabled_cls
from .temp_limit_rel_to_boil_point import temp_limit_rel_to_boil_point as temp_limit_rel_to_boil_point_cls

class temperature_limiter(Group):
    """
    'temperature_limiter' child.
    """

    fluent_name = "temperature-limiter"

    child_names = \
        ['leidenfrost_temp_postproc_enabled', 'enabled',
         'temp_limit_rel_to_boil_point']

    _child_classes = dict(
        leidenfrost_temp_postproc_enabled=leidenfrost_temp_postproc_enabled_cls,
        enabled=enabled_cls,
        temp_limit_rel_to_boil_point=temp_limit_rel_to_boil_point_cls,
    )

    return_type = "<object object at 0x7fd94d0e6010>"
