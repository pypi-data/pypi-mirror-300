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

from .background_1 import background as background_cls
from .color_filter import color_filter as color_filter_cls
from .foreground_1 import foreground as foreground_cls
from .on import on as on_cls
from .pixel_size import pixel_size as pixel_size_cls

class video(Group):
    fluent_name = ...
    child_names = ...
    background: background_cls = ...
    color_filter: color_filter_cls = ...
    foreground: foreground_cls = ...
    on: on_cls = ...
    pixel_size: pixel_size_cls = ...
    return_type = ...
