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

from .enabled_45 import enabled as enabled_cls
from .model_constant_a import model_constant_a as model_constant_a_cls
from .velocity_exponent import velocity_exponent as velocity_exponent_cls
from .transition_angle import transition_angle as transition_angle_cls
from .impact_angle_constant_b import impact_angle_constant_b as impact_angle_constant_b_cls
from .impact_angle_constant_c import impact_angle_constant_c as impact_angle_constant_c_cls
from .impact_angle_constant_w import impact_angle_constant_w as impact_angle_constant_w_cls
from .impact_angle_constant_x import impact_angle_constant_x as impact_angle_constant_x_cls
from .impact_angle_constant_y import impact_angle_constant_y as impact_angle_constant_y_cls

class mclaury(Group):
    """
    Settings for the McLaury erosion model.
    """

    fluent_name = "mclaury"

    child_names = \
        ['enabled', 'model_constant_a', 'velocity_exponent',
         'transition_angle', 'impact_angle_constant_b',
         'impact_angle_constant_c', 'impact_angle_constant_w',
         'impact_angle_constant_x', 'impact_angle_constant_y']

    _child_classes = dict(
        enabled=enabled_cls,
        model_constant_a=model_constant_a_cls,
        velocity_exponent=velocity_exponent_cls,
        transition_angle=transition_angle_cls,
        impact_angle_constant_b=impact_angle_constant_b_cls,
        impact_angle_constant_c=impact_angle_constant_c_cls,
        impact_angle_constant_w=impact_angle_constant_w_cls,
        impact_angle_constant_x=impact_angle_constant_x_cls,
        impact_angle_constant_y=impact_angle_constant_y_cls,
    )

    _child_aliases = dict(
        dpm_bc_erosion_mclaury_a="model_constant_a",
        dpm_bc_erosion_mclaury_b="impact_angle_constant_b",
        dpm_bc_erosion_mclaury_c="impact_angle_constant_c",
        dpm_bc_erosion_mclaury_transition_angle="transition_angle",
        dpm_bc_erosion_mclaury_vel_exp="velocity_exponent",
        dpm_bc_erosion_mclaury_w="impact_angle_constant_w",
        dpm_bc_erosion_mclaury_x="impact_angle_constant_x",
        dpm_bc_erosion_mclaury_y="impact_angle_constant_y",
        dpm_bc_erosion_mclaury="enabled",
    )

