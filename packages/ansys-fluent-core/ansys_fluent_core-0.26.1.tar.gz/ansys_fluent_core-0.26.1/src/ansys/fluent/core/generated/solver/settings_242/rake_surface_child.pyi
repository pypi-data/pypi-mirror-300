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
from .p0 import p0 as p0_cls
from .p1 import p1 as p1_cls
from .number_of_points import number_of_points as number_of_points_cls
from .display_4 import display as display_cls

class rake_surface_child(Group):
    fluent_name = ...
    child_names = ...
    name: name_cls = ...
    p0: p0_cls = ...
    p1: p1_cls = ...
    number_of_points: number_of_points_cls = ...
    command_names = ...

    def display(self, ):
        """
        Display a surface.
        """

