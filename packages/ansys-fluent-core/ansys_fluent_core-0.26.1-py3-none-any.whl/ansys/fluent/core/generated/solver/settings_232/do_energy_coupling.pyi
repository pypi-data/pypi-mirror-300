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

from .enable_4 import enable as enable_cls
from .solution_method import solution_method as solution_method_cls

class do_energy_coupling(Group):
    fluent_name = ...
    child_names = ...
    enable: enable_cls = ...
    solution_method: solution_method_cls = ...
    return_type = ...
