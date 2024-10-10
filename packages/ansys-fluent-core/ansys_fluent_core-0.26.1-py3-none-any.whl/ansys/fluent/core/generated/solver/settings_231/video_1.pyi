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

from .fps import fps as fps_cls
from .format_2 import format as format_cls
from .quality_1 import quality as quality_cls
from .name_4 import name as name_cls
from .use_original_resolution import use_original_resolution as use_original_resolution_cls
from .scale_4 import scale as scale_cls
from .set_standard_resolution import set_standard_resolution as set_standard_resolution_cls
from .width_2 import width as width_cls
from .height_2 import height as height_cls
from .advance_quality import advance_quality as advance_quality_cls

class video(Group):
    fluent_name = ...
    child_names = ...
    fps: fps_cls = ...
    format: format_cls = ...
    quality: quality_cls = ...
    name: name_cls = ...
    use_original_resolution: use_original_resolution_cls = ...
    scale: scale_cls = ...
    set_standard_resolution: set_standard_resolution_cls = ...
    width: width_cls = ...
    height: height_cls = ...
    advance_quality: advance_quality_cls = ...
    return_type = ...
