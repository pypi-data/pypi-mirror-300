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

from .mean_and_std_deviation import mean_and_std_deviation as mean_and_std_deviation_cls
from .pb_disc_components import pb_disc_components as pb_disc_components_cls

class pb_disc(Group):
    fluent_name = ...
    child_names = ...
    mean_and_std_deviation: mean_and_std_deviation_cls = ...
    pb_disc_components: pb_disc_components_cls = ...
    return_type = ...
