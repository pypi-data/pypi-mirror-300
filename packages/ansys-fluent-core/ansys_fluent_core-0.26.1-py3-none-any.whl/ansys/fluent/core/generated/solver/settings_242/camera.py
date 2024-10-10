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

from .dolly import dolly as dolly_cls
from .field_6 import field as field_cls
from .orbit import orbit as orbit_cls
from .pan import pan as pan_cls
from .position_1 import position as position_cls
from .projection import projection as projection_cls
from .roll import roll as roll_cls
from .target_1 import target as target_cls
from .up_vector import up_vector as up_vector_cls
from .zoom import zoom as zoom_cls

class camera(Group):
    """
    'camera' child.
    """

    fluent_name = "camera"

    command_names = \
        ['dolly', 'field', 'orbit', 'pan', 'position', 'projection', 'roll',
         'target', 'up_vector', 'zoom']

    _child_classes = dict(
        dolly=dolly_cls,
        field=field_cls,
        orbit=orbit_cls,
        pan=pan_cls,
        position=position_cls,
        projection=projection_cls,
        roll=roll_cls,
        target=target_cls,
        up_vector=up_vector_cls,
        zoom=zoom_cls,
    )

