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

from .always_use_face_centroid_with_periodics import always_use_face_centroid_with_periodics as always_use_face_centroid_with_periodics_cls
from .interpolation import interpolation as interpolation_cls
from .boundary_layer_tracking import boundary_layer_tracking as boundary_layer_tracking_cls
from .check_subtet_validity import check_subtet_validity as check_subtet_validity_cls
from .automatic_intersection_tolerance_enabled import automatic_intersection_tolerance_enabled as automatic_intersection_tolerance_enabled_cls
from .barycentric_intersection_enabled import barycentric_intersection_enabled as barycentric_intersection_enabled_cls
from .particle_relocation import particle_relocation as particle_relocation_cls
from .stuck_particle_removal_enabled import stuck_particle_removal_enabled as stuck_particle_removal_enabled_cls
from .barycentric_sampling_enabled import barycentric_sampling_enabled as barycentric_sampling_enabled_cls
from .quad_face_use_centroid_enabled import quad_face_use_centroid_enabled as quad_face_use_centroid_enabled_cls

class high_res_tracking_options(Group):
    """
    Main menu containing settings that control the High-Res Tracking scheme.
    When the High-Res Tracking option is enabled (default), the computational cells are decomposed into tetrahedrons
    (subtets) and the particles tracked through the subtets. This option provides a more robust tracking
    algorithm and improved variable interpolation. If High-Res Tracking is not enabled, particles are tracked through
    the computational cells directly. Flow variables that appear in particle equations either use cell-center values
    or a truncated Taylor series approximation for interpolation to the particle position.
    """

    fluent_name = "high-res-tracking-options"

    child_names = \
        ['always_use_face_centroid_with_periodics', 'interpolation',
         'boundary_layer_tracking', 'check_subtet_validity',
         'automatic_intersection_tolerance_enabled',
         'barycentric_intersection_enabled', 'particle_relocation',
         'stuck_particle_removal_enabled', 'barycentric_sampling_enabled',
         'quad_face_use_centroid_enabled']

    _child_classes = dict(
        always_use_face_centroid_with_periodics=always_use_face_centroid_with_periodics_cls,
        interpolation=interpolation_cls,
        boundary_layer_tracking=boundary_layer_tracking_cls,
        check_subtet_validity=check_subtet_validity_cls,
        automatic_intersection_tolerance_enabled=automatic_intersection_tolerance_enabled_cls,
        barycentric_intersection_enabled=barycentric_intersection_enabled_cls,
        particle_relocation=particle_relocation_cls,
        stuck_particle_removal_enabled=stuck_particle_removal_enabled_cls,
        barycentric_sampling_enabled=barycentric_sampling_enabled_cls,
        quad_face_use_centroid_enabled=quad_face_use_centroid_enabled_cls,
    )

    return_type = "<object object at 0x7fe5b9e4d840>"
