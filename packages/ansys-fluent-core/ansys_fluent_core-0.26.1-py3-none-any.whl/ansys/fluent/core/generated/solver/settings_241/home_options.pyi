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

from .field_name_1 import field_name as field_name_cls
from .data_source import data_source as data_source_cls
from .range_options import range_options as range_options_cls
from .rendering_quality import rendering_quality as rendering_quality_cls
from .color_density import color_density as color_density_cls
from .colormap_options import colormap_options as colormap_options_cls
from .cell_zones_3 import cell_zones as cell_zones_cls

class home_options(Group):
    fluent_name = ...
    child_names = ...
    field_name: field_name_cls = ...
    data_source: data_source_cls = ...
    range_options: range_options_cls = ...
    rendering_quality: rendering_quality_cls = ...
    color_density: color_density_cls = ...
    colormap_options: colormap_options_cls = ...
    cell_zones: cell_zones_cls = ...
    return_type = ...
