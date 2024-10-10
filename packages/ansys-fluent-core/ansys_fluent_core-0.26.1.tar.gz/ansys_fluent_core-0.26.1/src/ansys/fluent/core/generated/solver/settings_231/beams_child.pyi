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

from .ap_face_zone import ap_face_zone as ap_face_zone_cls
from .beam_length import beam_length as beam_length_cls
from .ray_points_count import ray_points_count as ray_points_count_cls
from .beam_vector import beam_vector as beam_vector_cls

class beams_child(Group):
    fluent_name = ...
    child_names = ...
    ap_face_zone: ap_face_zone_cls = ...
    beam_length: beam_length_cls = ...
    ray_points_count: ray_points_count_cls = ...
    beam_vector: beam_vector_cls = ...
    return_type = ...
