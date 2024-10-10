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

from .enable_10 import enable as enable_cls
from .mgrid_enable_transient import mgrid_enable_transient as mgrid_enable_transient_cls
from .mgrid_relative_to_thread import mgrid_relative_to_thread as mgrid_relative_to_thread_cls
from .mgrid_omega import mgrid_omega as mgrid_omega_cls
from .moving_mesh_velocity import moving_mesh_velocity as moving_mesh_velocity_cls
from .moving_mesh_axis_origin import moving_mesh_axis_origin as moving_mesh_axis_origin_cls
from .moving_mesh_axis_direction import moving_mesh_axis_direction as moving_mesh_axis_direction_cls
from .moving_mesh_zone_motion_function import moving_mesh_zone_motion_function as moving_mesh_zone_motion_function_cls

class mesh_motion(Group):
    """
    Help not available.
    """

    fluent_name = "mesh-motion"

    child_names = \
        ['enable', 'mgrid_enable_transient', 'mgrid_relative_to_thread',
         'mgrid_omega', 'moving_mesh_velocity', 'moving_mesh_axis_origin',
         'moving_mesh_axis_direction', 'moving_mesh_zone_motion_function']

    _child_classes = dict(
        enable=enable_cls,
        mgrid_enable_transient=mgrid_enable_transient_cls,
        mgrid_relative_to_thread=mgrid_relative_to_thread_cls,
        mgrid_omega=mgrid_omega_cls,
        moving_mesh_velocity=moving_mesh_velocity_cls,
        moving_mesh_axis_origin=moving_mesh_axis_origin_cls,
        moving_mesh_axis_direction=moving_mesh_axis_direction_cls,
        moving_mesh_zone_motion_function=moving_mesh_zone_motion_function_cls,
    )

    _child_aliases = dict(
        mgrid_motion="enable",
        mgrid_udf_zmotion_name="moving_mesh_zone_motion_function",
        moving_mesh_axis_direction_components="moving_mesh_axis_direction",
        moving_mesh_axis_origin_components="moving_mesh_axis_origin",
        moving_mesh_velocity_components="moving_mesh_velocity",
    )

