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

from .positive_electrode_zone import positive_electrode_zone as positive_electrode_zone_cls
from .electrolyte_zone import electrolyte_zone as electrolyte_zone_cls
from .negative_electrode_zone import negative_electrode_zone as negative_electrode_zone_cls

class zone_assignment(Group):
    fluent_name = ...
    child_names = ...
    positive_electrode_zone: positive_electrode_zone_cls = ...
    electrolyte_zone: electrolyte_zone_cls = ...
    negative_electrode_zone: negative_electrode_zone_cls = ...
    return_type = ...
