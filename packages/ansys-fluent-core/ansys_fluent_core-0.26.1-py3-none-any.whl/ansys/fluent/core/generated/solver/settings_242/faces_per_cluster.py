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

from .option_2 import option as option_cls
from .global_faces_per_surface_cluster import global_faces_per_surface_cluster as global_faces_per_surface_cluster_cls
from .maximum_faces_per_surface_cluster import maximum_faces_per_surface_cluster as maximum_faces_per_surface_cluster_cls

class faces_per_cluster(Group):
    """
    Settings for determining number of faces per cluster.
    """

    fluent_name = "faces-per-cluster"

    child_names = \
        ['option', 'global_faces_per_surface_cluster',
         'maximum_faces_per_surface_cluster']

    _child_classes = dict(
        option=option_cls,
        global_faces_per_surface_cluster=global_faces_per_surface_cluster_cls,
        maximum_faces_per_surface_cluster=maximum_faces_per_surface_cluster_cls,
    )

