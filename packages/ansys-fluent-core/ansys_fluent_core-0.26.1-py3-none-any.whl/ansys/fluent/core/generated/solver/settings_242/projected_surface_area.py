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

from .surfaces import surfaces as surfaces_cls
from .min_feature_size import min_feature_size as min_feature_size_cls
from .proj_plane_norm_comp import proj_plane_norm_comp as proj_plane_norm_comp_cls

class projected_surface_area(Command):
    """
    Print total area of the projection of a group of surfaces to a plane.
    
    Parameters
    ----------
        surfaces : List
            Select surface.
        min_feature_size : real
            'min_feature_size' child.
        proj_plane_norm_comp : List
            'proj_plane_norm_comp' child.
    
    """

    fluent_name = "projected-surface-area"

    argument_names = \
        ['surfaces', 'min_feature_size', 'proj_plane_norm_comp']

    _child_classes = dict(
        surfaces=surfaces_cls,
        min_feature_size=min_feature_size_cls,
        proj_plane_norm_comp=proj_plane_norm_comp_cls,
    )

