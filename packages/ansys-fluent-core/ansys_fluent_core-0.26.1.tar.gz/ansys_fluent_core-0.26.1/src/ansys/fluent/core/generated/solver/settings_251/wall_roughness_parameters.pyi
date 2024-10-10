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

from .ra import ra as ra_cls
from .rz import rz as rz_cls
from .rq import rq as rq_cls
from .rsm import rsm as rsm_cls

class wall_roughness_parameters(Group):
    fluent_name = ...
    child_names = ...
    ra: ra_cls = ...
    rz: rz_cls = ...
    rq: rq_cls = ...
    rsm: rsm_cls = ...
