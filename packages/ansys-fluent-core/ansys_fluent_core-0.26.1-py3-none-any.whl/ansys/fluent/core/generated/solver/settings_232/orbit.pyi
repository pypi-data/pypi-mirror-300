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

from .right import right as right_cls
from .up import up as up_cls

class orbit(Command):
    fluent_name = ...
    argument_names = ...
    right: right_cls = ...
    up: up_cls = ...
    return_type = ...
