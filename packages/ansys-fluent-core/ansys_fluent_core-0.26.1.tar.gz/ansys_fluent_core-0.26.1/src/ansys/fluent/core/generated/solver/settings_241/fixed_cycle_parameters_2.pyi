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

from .pre_sweeps_3 import pre_sweeps as pre_sweeps_cls
from .post_sweeps_2 import post_sweeps as post_sweeps_cls

class fixed_cycle_parameters(Group):
    fluent_name = ...
    child_names = ...
    pre_sweeps: pre_sweeps_cls = ...
    post_sweeps: post_sweeps_cls = ...
    return_type = ...
