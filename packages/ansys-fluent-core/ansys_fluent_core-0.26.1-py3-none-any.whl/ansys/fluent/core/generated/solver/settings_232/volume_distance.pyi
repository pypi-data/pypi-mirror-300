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

from .boundary_volume import boundary_volume as boundary_volume_cls
from .volume_growth import volume_growth as volume_growth_cls

class volume_distance(Group):
    fluent_name = ...
    child_names = ...
    boundary_volume: boundary_volume_cls = ...
    volume_growth: volume_growth_cls = ...
    return_type = ...
