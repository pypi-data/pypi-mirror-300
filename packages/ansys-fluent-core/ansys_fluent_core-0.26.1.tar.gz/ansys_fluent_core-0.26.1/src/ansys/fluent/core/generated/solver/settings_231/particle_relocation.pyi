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

from .enhanced_cell_relocation_method import enhanced_cell_relocation_method as enhanced_cell_relocation_method_cls
from .load_legacy_particles import load_legacy_particles as load_legacy_particles_cls
from .overset_relocation_robustness_level import overset_relocation_robustness_level as overset_relocation_robustness_level_cls
from .use_legacy_particle_location_method import use_legacy_particle_location_method as use_legacy_particle_location_method_cls

class particle_relocation(Group):
    fluent_name = ...
    child_names = ...
    enhanced_cell_relocation_method: enhanced_cell_relocation_method_cls = ...
    load_legacy_particles: load_legacy_particles_cls = ...
    overset_relocation_robustness_level: overset_relocation_robustness_level_cls = ...
    use_legacy_particle_location_method: use_legacy_particle_location_method_cls = ...
    return_type = ...
