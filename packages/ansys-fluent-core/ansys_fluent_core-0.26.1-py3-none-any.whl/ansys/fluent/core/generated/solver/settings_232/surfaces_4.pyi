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

from .point_surface import point_surface as point_surface_cls
from .line_surface import line_surface as line_surface_cls
from .rake_surface import rake_surface as rake_surface_cls
from .iso_surface import iso_surface as iso_surface_cls
from .plane_surface import plane_surface as plane_surface_cls

class surfaces(Group):
    fluent_name = ...
    child_names = ...
    point_surface: point_surface_cls = ...
    line_surface: line_surface_cls = ...
    rake_surface: rake_surface_cls = ...
    iso_surface: iso_surface_cls = ...
    plane_surface: plane_surface_cls = ...
    return_type = ...
