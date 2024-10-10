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

from .particle_forces import particle_forces as particle_forces_cls
from .erosion_accretion_enabled import erosion_accretion_enabled as erosion_accretion_enabled_cls
from .twoway_turb_coupl_enabled import twoway_turb_coupl_enabled as twoway_turb_coupl_enabled_cls
from .secondary_breakup_enabled import secondary_breakup_enabled as secondary_breakup_enabled_cls
from .volume_displacement import volume_displacement as volume_displacement_cls
from .wall_film import wall_film as wall_film_cls

class physical_models(Group):
    """
    Main menu to enable the required physical submodels for the discrete phase model.
    """

    fluent_name = "physical-models"

    child_names = \
        ['particle_forces', 'erosion_accretion_enabled',
         'twoway_turb_coupl_enabled', 'secondary_breakup_enabled',
         'volume_displacement', 'wall_film']

    _child_classes = dict(
        particle_forces=particle_forces_cls,
        erosion_accretion_enabled=erosion_accretion_enabled_cls,
        twoway_turb_coupl_enabled=twoway_turb_coupl_enabled_cls,
        secondary_breakup_enabled=secondary_breakup_enabled_cls,
        volume_displacement=volume_displacement_cls,
        wall_film=wall_film_cls,
    )

    _child_aliases = dict(
        pressure_force_enabled="particle_forces/pressure_force_enabled",
        pressure_gradient_force="particle_forces/pressure_gradient_force",
        saffman_lift_force_enabled="particle_forces/saffman_lift_force_enabled",
        thermophoretic_force_enabled="particle_forces/thermophoretic_force_enabled",
        virtual_mass_force="particle_forces/virtual_mass_force",
    )

