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

from .dispersion_force_in_momentum import dispersion_force_in_momentum as dispersion_force_in_momentum_cls
from .dispersion_in_relative_velocity import dispersion_in_relative_velocity as dispersion_in_relative_velocity_cls

class multiphase_options(Group):
    fluent_name = ...
    child_names = ...
    dispersion_force_in_momentum: dispersion_force_in_momentum_cls = ...
    dispersion_in_relative_velocity: dispersion_in_relative_velocity_cls = ...
