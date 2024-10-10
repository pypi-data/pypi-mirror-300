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

from .enabled_16 import enabled as enabled_cls
from .radius import radius as radius_cls
from .only_in_plane import only_in_plane as only_in_plane_cls

class spatial_staggering(Group):
    """
    Enable and configure spatial staggering.
    """

    fluent_name = "spatial-staggering"

    child_names = \
        ['enabled', 'radius', 'only_in_plane']

    _child_classes = dict(
        enabled=enabled_cls,
        radius=radius_cls,
        only_in_plane=only_in_plane_cls,
    )

