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

from .name_2 import name as name_cls
from .field_1 import field as field_cls
from .surfaces_6 import surfaces as surfaces_cls
from .range_2 import range as range_cls
from .display_4 import display as display_cls

class iso_clip_child(Group):
    """
    'child_object_type' of iso_clip.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'field', 'surfaces', 'range']

    command_names = \
        ['display']

    _child_classes = dict(
        name=name_cls,
        field=field_cls,
        surfaces=surfaces_cls,
        range=range_cls,
        display=display_cls,
    )

    _child_aliases = dict(
        max="range/maximum",
        min="range/minimum",
        update_min_max="range/compute",
    )

