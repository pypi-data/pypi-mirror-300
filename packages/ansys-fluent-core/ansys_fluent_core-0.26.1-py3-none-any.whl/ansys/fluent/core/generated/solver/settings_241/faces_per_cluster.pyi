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

from .option_1 import option as option_cls
from .global_faces_per_surface_cluster import global_faces_per_surface_cluster as global_faces_per_surface_cluster_cls
from .maximum_faces_per_surface_cluster import maximum_faces_per_surface_cluster as maximum_faces_per_surface_cluster_cls

class faces_per_cluster(Group):
    fluent_name = ...
    child_names = ...
    option: option_cls = ...
    global_faces_per_surface_cluster: global_faces_per_surface_cluster_cls = ...
    maximum_faces_per_surface_cluster: maximum_faces_per_surface_cluster_cls = ...
    return_type = ...
