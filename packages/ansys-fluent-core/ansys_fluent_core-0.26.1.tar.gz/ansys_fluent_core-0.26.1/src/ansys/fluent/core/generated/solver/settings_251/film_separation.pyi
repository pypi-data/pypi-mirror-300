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

from .model_5 import model as model_cls
from .critical_weber_number_1 import critical_weber_number as critical_weber_number_cls
from .separation_angle import separation_angle as separation_angle_cls

class film_separation(Group):
    fluent_name = ...
    child_names = ...
    model: model_cls = ...
    critical_weber_number: critical_weber_number_cls = ...
    separation_angle: separation_angle_cls = ...
