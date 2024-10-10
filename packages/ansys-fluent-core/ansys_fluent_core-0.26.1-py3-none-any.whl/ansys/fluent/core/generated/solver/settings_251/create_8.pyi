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

from .name_20 import name as name_cls
from .surfaces_7 import surfaces as surfaces_cls

class create(CommandWithPositionalArgs):
    fluent_name = ...
    argument_names = ...
    name: name_cls = ...
    surfaces: surfaces_cls = ...
