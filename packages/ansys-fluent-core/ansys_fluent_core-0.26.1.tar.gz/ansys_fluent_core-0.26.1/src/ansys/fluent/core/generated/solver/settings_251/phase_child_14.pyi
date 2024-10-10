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

from typing import Union, List, Tuple

from .network_end import network_end as network_end_cls
from .adjacent_cell_zone import adjacent_cell_zone as adjacent_cell_zone_cls
from .shadow_face_zone import shadow_face_zone as shadow_face_zone_cls

class phase_child(Group):
    fluent_name = ...
    child_names = ...
    network_end: network_end_cls = ...
    query_names = ...

    def adjacent_cell_zone(self, ):
        """
        Get adjacent cell zone for this face zone.
        """

    def shadow_face_zone(self, ):
        """
        Get shadow zone for this wall zone.
        """

