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

from .name_19 import name as name_cls
from .custom_field_function import custom_field_function as custom_field_function_cls

class create(CommandWithPositionalArgs):
    fluent_name = ...
    argument_names = ...
    name: name_cls = ...
    custom_field_function: custom_field_function_cls = ...
