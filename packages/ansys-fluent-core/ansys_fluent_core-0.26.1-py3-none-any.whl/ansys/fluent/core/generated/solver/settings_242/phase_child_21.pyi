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

from .momentum_8 import momentum as momentum_cls
from .turbulence_1 import turbulence as turbulence_cls
from .thermal_1 import thermal as thermal_cls
from .radiation_2 import radiation as radiation_cls
from .species_6 import species as species_cls
from .dpm import dpm as dpm_cls
from .multiphase_3 import multiphase as multiphase_cls
from .potential_1 import potential as potential_cls
from .structure_1 import structure as structure_cls
from .uds_1 import uds as uds_cls
from .icing_1 import icing as icing_cls
from .geometry_3 import geometry as geometry_cls
from .adjacent_cell_zone import adjacent_cell_zone as adjacent_cell_zone_cls
from .shadow_face_zone import shadow_face_zone as shadow_face_zone_cls

class phase_child(Group):
    fluent_name = ...
    child_names = ...
    momentum: momentum_cls = ...
    turbulence: turbulence_cls = ...
    thermal: thermal_cls = ...
    radiation: radiation_cls = ...
    species: species_cls = ...
    dpm: dpm_cls = ...
    multiphase: multiphase_cls = ...
    potential: potential_cls = ...
    structure: structure_cls = ...
    uds: uds_cls = ...
    icing: icing_cls = ...
    geometry: geometry_cls = ...
    query_names = ...

    def adjacent_cell_zone(self, ):
        """
        Get adjacent cell zone for this face zone.
        """

    def shadow_face_zone(self, ):
        """
        Get shadow zone for this wall zone.
        """

