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

from .enable_volumetric_reactions import enable_volumetric_reactions as enable_volumetric_reactions_cls
from .enable_wall_surface import enable_wall_surface as enable_wall_surface_cls
from .enable_particle_surface import enable_particle_surface as enable_particle_surface_cls
from .enable_electrochemical_surface import enable_electrochemical_surface as enable_electrochemical_surface_cls

class reactions(Group):
    fluent_name = ...
    child_names = ...
    enable_volumetric_reactions: enable_volumetric_reactions_cls = ...
    enable_wall_surface: enable_wall_surface_cls = ...
    enable_particle_surface: enable_particle_surface_cls = ...
    enable_electrochemical_surface: enable_electrochemical_surface_cls = ...
    return_type = ...
