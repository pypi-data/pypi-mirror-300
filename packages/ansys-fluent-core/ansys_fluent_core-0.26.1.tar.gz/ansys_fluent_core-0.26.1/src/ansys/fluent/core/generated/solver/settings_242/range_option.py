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
from .auto_range_on import auto_range_on as auto_range_on_cls
from .auto_range_off import auto_range_off as auto_range_off_cls

class range_option(Group):
    """
    Specify whether you want the range to be Global, Local to the selected surface(s), or Custom.
    """

    fluent_name = "range-option"

    child_names = \
        ['option', 'auto_range_on', 'auto_range_off']

    _child_classes = dict(
        option=option_cls,
        auto_range_on=auto_range_on_cls,
        auto_range_off=auto_range_off_cls,
    )

