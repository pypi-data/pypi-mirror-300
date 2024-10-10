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

from .name import name as name_cls
from .phase import phase as phase_cls
from .general_2 import general as general_cls
from .conical import conical as conical_cls
from .reference_frame_2 import reference_frame as reference_frame_cls
from .mesh_motion import mesh_motion as mesh_motion_cls
from .zonal_models_1 import zonal_models as zonal_models_cls
from .porous_zone import porous_zone as porous_zone_cls
from .fan_zone_1 import fan_zone as fan_zone_cls
from .embedded_les import embedded_les as embedded_les_cls
from .reaction import reaction as reaction_cls
from .sources import sources as sources_cls
from .fixed_values import fixed_values as fixed_values_cls
from .multiphase_1 import multiphase as multiphase_cls
from .disabled import disabled as disabled_cls
from .adjacent_cell_zone import adjacent_cell_zone as adjacent_cell_zone_cls
from .shadow_face_zone import shadow_face_zone as shadow_face_zone_cls

class fluid_child(Group):
    fluent_name = ...
    child_names = ...
    name: name_cls = ...
    phase: phase_cls = ...
    general: general_cls = ...
    conical: conical_cls = ...
    reference_frame: reference_frame_cls = ...
    mesh_motion: mesh_motion_cls = ...
    zonal_models: zonal_models_cls = ...
    porous_zone: porous_zone_cls = ...
    fan_zone: fan_zone_cls = ...
    embedded_les: embedded_les_cls = ...
    reaction: reaction_cls = ...
    sources: sources_cls = ...
    fixed_values: fixed_values_cls = ...
    multiphase: multiphase_cls = ...
    disabled: disabled_cls = ...
    query_names = ...

    def adjacent_cell_zone(self, ):
        """
        Get adjacent cell zone for this face zone.
        """

    def shadow_face_zone(self, ):
        """
        Get shadow zone for this wall zone.
        """

