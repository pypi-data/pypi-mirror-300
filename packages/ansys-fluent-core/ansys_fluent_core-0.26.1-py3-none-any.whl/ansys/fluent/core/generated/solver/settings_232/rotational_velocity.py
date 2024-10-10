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

from .speed import speed as speed_cls
from .rotation_axis import rotation_axis as rotation_axis_cls

class rotational_velocity(Group):
    """
    'rotational_velocity' child.
    """

    fluent_name = "rotational-velocity"

    child_names = \
        ['speed', 'rotation_axis']

    _child_classes = dict(
        speed=speed_cls,
        rotation_axis=rotation_axis_cls,
    )

    return_type = "<object object at 0x7fe5b915ebc0>"
