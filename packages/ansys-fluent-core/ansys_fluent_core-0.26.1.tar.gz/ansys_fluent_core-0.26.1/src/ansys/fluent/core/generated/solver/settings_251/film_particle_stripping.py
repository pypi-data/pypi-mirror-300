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

from .enabled_40 import enabled as enabled_cls
from .critical_shear_stress import critical_shear_stress as critical_shear_stress_cls

class film_particle_stripping(Group):
    """
    Settings for stripping of particles from the film.
    """

    fluent_name = "film-particle-stripping"

    child_names = \
        ['enabled', 'critical_shear_stress']

    _child_classes = dict(
        enabled=enabled_cls,
        critical_shear_stress=critical_shear_stress_cls,
    )

    _child_aliases = dict(
        dpm_crit_stripping_const="critical_shear_stress",
        dpm_film_stripping="enabled",
    )

