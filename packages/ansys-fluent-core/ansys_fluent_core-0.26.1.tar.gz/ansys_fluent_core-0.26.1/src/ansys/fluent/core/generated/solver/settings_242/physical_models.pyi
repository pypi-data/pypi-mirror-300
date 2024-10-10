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

from .pressure_gradient_force import pressure_gradient_force as pressure_gradient_force_cls
from .saffman_lift_force_enabled import saffman_lift_force_enabled as saffman_lift_force_enabled_cls
from .pressure_force_enabled import pressure_force_enabled as pressure_force_enabled_cls
from .virtual_mass_force import virtual_mass_force as virtual_mass_force_cls
from .thermophoretic_force_enabled import thermophoretic_force_enabled as thermophoretic_force_enabled_cls
from .erosion_accretion_enabled import erosion_accretion_enabled as erosion_accretion_enabled_cls
from .twoway_turb_coupl_enabled import twoway_turb_coupl_enabled as twoway_turb_coupl_enabled_cls
from .secondary_breakup_enabled import secondary_breakup_enabled as secondary_breakup_enabled_cls
from .volume_displacement import volume_displacement as volume_displacement_cls
from .wall_film import wall_film as wall_film_cls

class physical_models(Group):
    fluent_name = ...
    child_names = ...
    pressure_gradient_force: pressure_gradient_force_cls = ...
    saffman_lift_force_enabled: saffman_lift_force_enabled_cls = ...
    pressure_force_enabled: pressure_force_enabled_cls = ...
    virtual_mass_force: virtual_mass_force_cls = ...
    thermophoretic_force_enabled: thermophoretic_force_enabled_cls = ...
    erosion_accretion_enabled: erosion_accretion_enabled_cls = ...
    twoway_turb_coupl_enabled: twoway_turb_coupl_enabled_cls = ...
    secondary_breakup_enabled: secondary_breakup_enabled_cls = ...
    volume_displacement: volume_displacement_cls = ...
    wall_film: wall_film_cls = ...
