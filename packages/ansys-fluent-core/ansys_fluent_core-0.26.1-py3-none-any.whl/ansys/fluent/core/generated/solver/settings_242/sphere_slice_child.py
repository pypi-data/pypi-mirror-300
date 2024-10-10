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
from .center_1 import center as center_cls
from .radius_1 import radius as radius_cls
from .display_4 import display as display_cls

class sphere_slice_child(Group):
    """
    'child_object_type' of sphere_slice.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'center', 'radius']

    command_names = \
        ['display']

    _child_classes = dict(
        name=name_cls,
        center=center_cls,
        radius=radius_cls,
        display=display_cls,
    )

