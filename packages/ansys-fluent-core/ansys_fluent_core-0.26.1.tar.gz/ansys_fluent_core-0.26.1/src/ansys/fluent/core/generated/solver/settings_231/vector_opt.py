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

from .in_plane import in_plane as in_plane_cls
from .fixed_length import fixed_length as fixed_length_cls
from .x_comp import x_comp as x_comp_cls
from .y_comp import y_comp as y_comp_cls
from .z_comp import z_comp as z_comp_cls
from .scale_head import scale_head as scale_head_cls
from .color import color as color_cls

class vector_opt(Group):
    """
    'vector_opt' child.
    """

    fluent_name = "vector-opt"

    child_names = \
        ['in_plane', 'fixed_length', 'x_comp', 'y_comp', 'z_comp',
         'scale_head', 'color']

    _child_classes = dict(
        in_plane=in_plane_cls,
        fixed_length=fixed_length_cls,
        x_comp=x_comp_cls,
        y_comp=y_comp_cls,
        z_comp=z_comp_cls,
        scale_head=scale_head_cls,
        color=color_cls,
    )

    return_type = "<object object at 0x7ff9d0a63c00>"
