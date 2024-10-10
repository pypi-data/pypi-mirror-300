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

from .viscous_scale import viscous_scale as viscous_scale_cls
from .gravity_scale import gravity_scale as gravity_scale_cls
from .surface_tension_scale import surface_tension_scale as surface_tension_scale_cls
from .acoustic_scale import acoustic_scale as acoustic_scale_cls

class time_scale_options(Group):
    fluent_name = ...
    child_names = ...
    viscous_scale: viscous_scale_cls = ...
    gravity_scale: gravity_scale_cls = ...
    surface_tension_scale: surface_tension_scale_cls = ...
    acoustic_scale: acoustic_scale_cls = ...
    return_type = ...
