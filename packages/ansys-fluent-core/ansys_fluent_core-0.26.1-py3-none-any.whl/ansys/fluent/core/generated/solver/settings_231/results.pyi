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

from .graphics import graphics as graphics_cls
from .scene import scene as scene_cls
from .surfaces_2 import surfaces as surfaces_cls
from .animations import animations as animations_cls
from .plot_2 import plot as plot_cls
from .report_1 import report as report_cls

class results(Group):
    fluent_name = ...
    child_names = ...
    graphics: graphics_cls = ...
    scene: scene_cls = ...
    surfaces: surfaces_cls = ...
    animations: animations_cls = ...
    plot: plot_cls = ...
    report: report_cls = ...
    return_type = ...
