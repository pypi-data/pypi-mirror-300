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

from .name_6 import name as name_cls
from .ap_face_zone import ap_face_zone as ap_face_zone_cls
from .beam_length import beam_length as beam_length_cls
from .ray_points_count import ray_points_count as ray_points_count_cls
from .beam_vector import beam_vector as beam_vector_cls

class create(CommandWithPositionalArgs):
    """
    Copy optical beam grid.
    
    Parameters
    ----------
        name : str
            Set a unique name for each optical beam.
        ap_face_zone : str
            Set the wall face zones to specify the optical aperture surface.
        beam_length : real
            Set the length of optical beam propagation.
        ray_points_count : int
            Set the number of grid point in each ray of the optical beam.
        beam_vector : List
            Set the components of the beam propagation vector.
    
    """

    fluent_name = "create"

    argument_names = \
        ['name', 'ap_face_zone', 'beam_length', 'ray_points_count',
         'beam_vector']

    _child_classes = dict(
        name=name_cls,
        ap_face_zone=ap_face_zone_cls,
        beam_length=beam_length_cls,
        ray_points_count=ray_points_count_cls,
        beam_vector=beam_vector_cls,
    )

