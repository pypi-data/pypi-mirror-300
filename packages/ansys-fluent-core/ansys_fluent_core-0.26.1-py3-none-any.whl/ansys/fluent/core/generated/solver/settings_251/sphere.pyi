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

from .center import center as center_cls
from .radius_1 import radius as radius_cls
from .inside import inside as inside_cls

class sphere(Group):
    fluent_name = ...
    child_names = ...
    center: center_cls = ...
    radius: radius_cls = ...
    inside: inside_cls = ...
