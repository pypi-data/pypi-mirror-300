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

from .surfaces_8 import surfaces as surfaces_cls
from .name_11 import name as name_cls

class create_group_surfaces(Command):
    fluent_name = ...
    argument_names = ...
    surfaces: surfaces_cls = ...
    name: name_cls = ...
