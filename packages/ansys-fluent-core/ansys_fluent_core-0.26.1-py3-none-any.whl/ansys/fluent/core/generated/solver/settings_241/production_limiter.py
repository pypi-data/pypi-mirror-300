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

from .enabled_1 import enabled as enabled_cls
from .clip_factor import clip_factor as clip_factor_cls

class production_limiter(Group):
    """
    'production_limiter' child.
    """

    fluent_name = "production-limiter"

    child_names = \
        ['enabled', 'clip_factor']

    _child_classes = dict(
        enabled=enabled_cls,
        clip_factor=clip_factor_cls,
    )

    return_type = "<object object at 0x7fd94e3ed3c0>"
