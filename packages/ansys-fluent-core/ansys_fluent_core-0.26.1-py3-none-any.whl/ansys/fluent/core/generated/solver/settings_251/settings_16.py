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

from .momentum_5 import momentum as momentum_cls
from .potential_1 import potential as potential_cls
from .structure_1 import structure as structure_cls
from .uds_2 import uds as uds_cls
from .radiation_4 import radiation as radiation_cls
from .discrete_phase_4 import discrete_phase as discrete_phase_cls
from .geometry_2 import geometry as geometry_cls
from .phase_44 import phase as phase_cls

class settings(Group):
    """
    Select domain name to define settings on.
    """

    fluent_name = "settings"

    child_names = \
        ['momentum', 'potential', 'structure', 'uds', 'radiation',
         'discrete_phase', 'geometry', 'phase']

    _child_classes = dict(
        momentum=momentum_cls,
        potential=potential_cls,
        structure=structure_cls,
        uds=uds_cls,
        radiation=radiation_cls,
        discrete_phase=discrete_phase_cls,
        geometry=geometry_cls,
        phase=phase_cls,
    )

    _child_aliases = dict(
        dpm="discrete_phase",
    )

