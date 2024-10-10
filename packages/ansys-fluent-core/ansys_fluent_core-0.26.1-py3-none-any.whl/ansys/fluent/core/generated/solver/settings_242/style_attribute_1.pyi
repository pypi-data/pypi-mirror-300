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

from .style_1 import style as style_cls
from .line_width import line_width as line_width_cls
from .arrow_space import arrow_space as arrow_space_cls
from .arrow_scale import arrow_scale as arrow_scale_cls
from .marker_size_1 import marker_size as marker_size_cls
from .sphere_size import sphere_size as sphere_size_cls
from .sphere_lod import sphere_lod as sphere_lod_cls
from .radius import radius as radius_cls
from .ribbon_settings import ribbon_settings as ribbon_settings_cls
from .sphere_settings import sphere_settings as sphere_settings_cls

class style_attribute(Group):
    fluent_name = ...
    child_names = ...
    style: style_cls = ...
    line_width: line_width_cls = ...
    arrow_space: arrow_space_cls = ...
    arrow_scale: arrow_scale_cls = ...
    marker_size: marker_size_cls = ...
    sphere_size: sphere_size_cls = ...
    sphere_lod: sphere_lod_cls = ...
    radius: radius_cls = ...
    ribbon_settings: ribbon_settings_cls = ...
    sphere_settings: sphere_settings_cls = ...
