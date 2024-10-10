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

from .field import field as field_cls
from .options_13 import options as options_cls
from .enabled_15 import enabled as enabled_cls
from .filter_minimum import filter_minimum as filter_minimum_cls
from .filter_maximum import filter_maximum as filter_maximum_cls

class filter_settings(Group):
    """
    'filter_settings' child.
    """

    fluent_name = "filter-settings"

    child_names = \
        ['field', 'options', 'enabled', 'filter_minimum', 'filter_maximum']

    _child_classes = dict(
        field=field_cls,
        options=options_cls,
        enabled=enabled_cls,
        filter_minimum=filter_minimum_cls,
        filter_maximum=filter_maximum_cls,
    )

    return_type = "<object object at 0x7fd93f8cc5c0>"
