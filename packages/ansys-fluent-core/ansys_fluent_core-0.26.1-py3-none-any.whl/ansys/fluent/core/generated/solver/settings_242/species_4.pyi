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

from .particle_species import particle_species as particle_species_cls
from .particle import particle as particle_cls
from .last_species import last_species as last_species_cls
from .material_3 import material as material_cls

class species(Group):
    fluent_name = ...
    child_names = ...
    particle_species: particle_species_cls = ...
    particle: particle_cls = ...
    last_species: last_species_cls = ...
    material: material_cls = ...
