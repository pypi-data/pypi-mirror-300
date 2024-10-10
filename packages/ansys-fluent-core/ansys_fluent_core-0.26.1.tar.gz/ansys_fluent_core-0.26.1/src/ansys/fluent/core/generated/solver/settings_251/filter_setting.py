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

from .enabled_66 import enabled as enabled_cls
from .field_9 import field as field_cls
from .option_48 import option as option_cls
from .range_4 import range as range_cls

class filter_setting(Group):
    """
    Specifies Particle Tracks Filter Settings.
    """

    fluent_name = "filter-setting"

    child_names = \
        ['enabled', 'field', 'option', 'range']

    _child_classes = dict(
        enabled=enabled_cls,
        field=field_cls,
        option=option_cls,
        range=range_cls,
    )

