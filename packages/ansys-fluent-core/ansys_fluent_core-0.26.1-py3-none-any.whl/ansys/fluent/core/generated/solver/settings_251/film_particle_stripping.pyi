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

from .enabled_40 import enabled as enabled_cls
from .critical_shear_stress import critical_shear_stress as critical_shear_stress_cls

class film_particle_stripping(Group):
    fluent_name = ...
    child_names = ...
    enabled: enabled_cls = ...
    critical_shear_stress: critical_shear_stress_cls = ...
