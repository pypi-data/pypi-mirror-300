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

from .name import name as name_cls
from .field_1 import field as field_cls
from .surfaces_6 import surfaces as surfaces_cls
from .min_4 import min as min_cls
from .max_4 import max as max_cls
from .display_4 import display as display_cls

class iso_clip_child(Group):
    """
    'child_object_type' of iso_clip.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'field', 'surfaces', 'min', 'max']

    command_names = \
        ['display']

    _child_classes = dict(
        name=name_cls,
        field=field_cls,
        surfaces=surfaces_cls,
        min=min_cls,
        max=max_cls,
        display=display_cls,
    )

