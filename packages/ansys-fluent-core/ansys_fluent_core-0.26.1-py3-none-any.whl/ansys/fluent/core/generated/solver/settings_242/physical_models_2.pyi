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

from .use_multi_physics import use_multi_physics as use_multi_physics_cls
from .threshold import threshold as threshold_cls
from .interval import interval as interval_cls

class physical_models(Group):
    fluent_name = ...
    child_names = ...
    use_multi_physics: use_multi_physics_cls = ...
    threshold: threshold_cls = ...
    interval: interval_cls = ...
