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

from .enabled_19 import enabled as enabled_cls
from .drag_law import drag_law as drag_law_cls
from .lift_law import lift_law as lift_law_cls

class particle_rotation(Group):
    """
    Help for this object class is not available without an instantiated object.
    """

    fluent_name = "particle-rotation"

    child_names = \
        ['enabled', 'drag_law', 'lift_law']

    _child_classes = dict(
        enabled=enabled_cls,
        drag_law=drag_law_cls,
        lift_law=lift_law_cls,
    )

