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

from .style import style as style_cls
from .vector_length import vector_length as vector_length_cls
from .constant_color import constant_color as constant_color_cls
from .vector_of import vector_of as vector_of_cls
from .scale_4 import scale as scale_cls
from .length_to_head_ratio import length_to_head_ratio as length_to_head_ratio_cls

class vector_settings(Group):
    fluent_name = ...
    child_names = ...
    style: style_cls = ...
    vector_length: vector_length_cls = ...
    constant_color: constant_color_cls = ...
    vector_of: vector_of_cls = ...
    scale: scale_cls = ...
    length_to_head_ratio: length_to_head_ratio_cls = ...
    return_type = ...
