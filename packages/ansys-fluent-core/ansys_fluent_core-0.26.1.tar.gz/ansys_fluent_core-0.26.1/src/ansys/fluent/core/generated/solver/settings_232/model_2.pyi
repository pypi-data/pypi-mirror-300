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

from .option import option as option_cls
from .material import material as material_cls
from .phase_material import phase_material as phase_material_cls

class model(Group):
    fluent_name = ...
    child_names = ...
    option: option_cls = ...
    material: material_cls = ...
    phase_material: phase_material_cls = ...
    return_type = ...
