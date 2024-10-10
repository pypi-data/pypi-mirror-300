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
from .method_2 import method as method_cls
from .x_3 import x as x_cls
from .y_3 import y as y_cls
from .z_1 import z as z_cls
from .point_vector import point_vector as point_vector_cls
from .point_normal import point_normal as point_normal_cls
from .surface_aligned_normal import surface_aligned_normal as surface_aligned_normal_cls
from .p0 import p0 as p0_cls
from .p1 import p1 as p1_cls
from .p2 import p2 as p2_cls
from .bounded import bounded as bounded_cls
from .sample_point import sample_point as sample_point_cls
from .edges import edges as edges_cls
from .display_3 import display as display_cls

class plane_surface_child(Group):
    fluent_name = ...
    child_names = ...
    name: name_cls = ...
    method: method_cls = ...
    x: x_cls = ...
    y: y_cls = ...
    z: z_cls = ...
    point_vector: point_vector_cls = ...
    point_normal: point_normal_cls = ...
    surface_aligned_normal: surface_aligned_normal_cls = ...
    p0: p0_cls = ...
    p1: p1_cls = ...
    p2: p2_cls = ...
    bounded: bounded_cls = ...
    sample_point: sample_point_cls = ...
    edges: edges_cls = ...
    command_names = ...

    def display(self, ):
        """
        'display' command.
        """

    return_type = ...
