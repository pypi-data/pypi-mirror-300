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

from .name import name as name_cls
from .attribute import attribute as attribute_cls
from .value_15 import value as value_cls
from .display_4 import display as display_cls

class quadric_surface_child(Group):
    fluent_name = ...
    child_names = ...
    name: name_cls = ...
    attribute: attribute_cls = ...
    value: value_cls = ...
    command_names = ...

    def display(self, ):
        """
        Display a surface.
        """

