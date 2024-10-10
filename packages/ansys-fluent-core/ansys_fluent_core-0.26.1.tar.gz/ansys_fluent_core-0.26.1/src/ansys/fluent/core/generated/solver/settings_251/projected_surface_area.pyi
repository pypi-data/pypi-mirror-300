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

from .surfaces import surfaces as surfaces_cls
from .min_feature_size import min_feature_size as min_feature_size_cls
from .proj_plane_norm_comp import proj_plane_norm_comp as proj_plane_norm_comp_cls

class projected_surface_area(Command):
    fluent_name = ...
    argument_names = ...
    surfaces: surfaces_cls = ...
    min_feature_size: min_feature_size_cls = ...
    proj_plane_norm_comp: proj_plane_norm_comp_cls = ...
