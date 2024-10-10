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

from .name_1 import name as name_cls
from .uid import uid as uid_cls
from .options_10 import options as options_cls
from .plot_direction import plot_direction as plot_direction_cls
from .x_axis_function import x_axis_function as x_axis_function_cls
from .y_axis_function import y_axis_function as y_axis_function_cls
from .surfaces_list import surfaces_list as surfaces_list_cls
from .physics import physics as physics_cls
from .geometry_3 import geometry as geometry_cls
from .surfaces import surfaces as surfaces_cls
from .axes import axes as axes_cls
from .curves import curves as curves_cls
from .display_2 import display as display_cls

class xy_plot_child(Group):
    fluent_name = ...
    child_names = ...
    name: name_cls = ...
    uid: uid_cls = ...
    options: options_cls = ...
    plot_direction: plot_direction_cls = ...
    x_axis_function: x_axis_function_cls = ...
    y_axis_function: y_axis_function_cls = ...
    surfaces_list: surfaces_list_cls = ...
    physics: physics_cls = ...
    geometry: geometry_cls = ...
    surfaces: surfaces_cls = ...
    axes: axes_cls = ...
    curves: curves_cls = ...
    command_names = ...

    def display(self, ):
        """
        'display' command.
        """

    return_type = ...
