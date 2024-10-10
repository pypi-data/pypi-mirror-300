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

from .enabled_1 import enabled as enabled_cls
from .ccurv import ccurv as ccurv_cls

class curvature_correction(Group):
    fluent_name = ...
    child_names = ...
    enabled: enabled_cls = ...
    ccurv: ccurv_cls = ...
