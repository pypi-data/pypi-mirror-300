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

from .enabled_44 import enabled as enabled_cls
from .model_constant_k import model_constant_k as model_constant_k_cls
from .velocity_exponent import velocity_exponent as velocity_exponent_cls
from .angle_of_max_erosion import angle_of_max_erosion as angle_of_max_erosion_cls

class finnie(Group):
    """
    Settings for the Finnie erosion model.
    """

    fluent_name = "finnie"

    child_names = \
        ['enabled', 'model_constant_k', 'velocity_exponent',
         'angle_of_max_erosion']

    _child_classes = dict(
        enabled=enabled_cls,
        model_constant_k=model_constant_k_cls,
        velocity_exponent=velocity_exponent_cls,
        angle_of_max_erosion=angle_of_max_erosion_cls,
    )

    _child_aliases = dict(
        dpm_bc_erosion_finnie_k="model_constant_k",
        dpm_bc_erosion_finnie_max_erosion_angle="angle_of_max_erosion",
        dpm_bc_erosion_finnie_vel_exp="velocity_exponent",
        dpm_bc_erosion_finnie="enabled",
    )

