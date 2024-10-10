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

from .evaporating_species import evaporating_species as evaporating_species_cls
from .continuous_phase import continuous_phase as continuous_phase_cls
from .volume_displacement_1 import volume_displacement as volume_displacement_cls

class interaction(Group):
    """
    Help for this object class is not available without an instantiated object.
    """

    fluent_name = "interaction"

    child_names = \
        ['evaporating_species', 'continuous_phase', 'volume_displacement']

    _child_classes = dict(
        evaporating_species=evaporating_species_cls,
        continuous_phase=continuous_phase_cls,
        volume_displacement=volume_displacement_cls,
    )

