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

from .implicit_body_force import implicit_body_force as implicit_body_force_cls
from .explicit_expert_options import explicit_expert_options as explicit_expert_options_cls

class advanced_formulation(Group):
    fluent_name = ...
    child_names = ...
    implicit_body_force: implicit_body_force_cls = ...
    explicit_expert_options: explicit_expert_options_cls = ...
