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

from .clip_to_range import clip_to_range as clip_to_range_cls
from .minimum_1 import minimum as minimum_cls
from .maximum_1 import maximum as maximum_cls

class auto_range_off(Group):
    """
    'auto_range_off' child.
    """

    fluent_name = "auto-range-off"

    child_names = \
        ['clip_to_range', 'minimum', 'maximum']

    _child_classes = dict(
        clip_to_range=clip_to_range_cls,
        minimum=minimum_cls,
        maximum=maximum_cls,
    )

    return_type = "<object object at 0x7fe5b8f45a50>"
