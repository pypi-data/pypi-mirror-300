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

from .max_vel_mag import max_vel_mag as max_vel_mag_cls
from .vol_frac_cutoff import vol_frac_cutoff as vol_frac_cutoff_cls

class set_velocity_and_vof_cutoffs_child(Group):
    fluent_name = ...
    child_names = ...
    max_vel_mag: max_vel_mag_cls = ...
    vol_frac_cutoff: vol_frac_cutoff_cls = ...
