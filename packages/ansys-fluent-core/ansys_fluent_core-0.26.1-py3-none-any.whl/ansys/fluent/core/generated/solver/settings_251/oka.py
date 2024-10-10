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

from .enabled_46 import enabled as enabled_cls
from .reference_erosion_rate_e90 import reference_erosion_rate_e90 as reference_erosion_rate_e90_cls
from .wall_vickers_hardness_hv import wall_vickers_hardness_hv as wall_vickers_hardness_hv_cls
from .model_constant_n1 import model_constant_n1 as model_constant_n1_cls
from .model_constant_n2 import model_constant_n2 as model_constant_n2_cls
from .velocity_exponent_k2 import velocity_exponent_k2 as velocity_exponent_k2_cls
from .diameter_exponent_k3 import diameter_exponent_k3 as diameter_exponent_k3_cls
from .reference_diameter_dref import reference_diameter_dref as reference_diameter_dref_cls
from .reference_velocity_vref import reference_velocity_vref as reference_velocity_vref_cls

class oka(Group):
    """
    Settings for the Oka erosion model.
    """

    fluent_name = "oka"

    child_names = \
        ['enabled', 'reference_erosion_rate_e90', 'wall_vickers_hardness_hv',
         'model_constant_n1', 'model_constant_n2', 'velocity_exponent_k2',
         'diameter_exponent_k3', 'reference_diameter_dref',
         'reference_velocity_vref']

    _child_classes = dict(
        enabled=enabled_cls,
        reference_erosion_rate_e90=reference_erosion_rate_e90_cls,
        wall_vickers_hardness_hv=wall_vickers_hardness_hv_cls,
        model_constant_n1=model_constant_n1_cls,
        model_constant_n2=model_constant_n2_cls,
        velocity_exponent_k2=velocity_exponent_k2_cls,
        diameter_exponent_k3=diameter_exponent_k3_cls,
        reference_diameter_dref=reference_diameter_dref_cls,
        reference_velocity_vref=reference_velocity_vref_cls,
    )

    _child_aliases = dict(
        dpm_bc_erosion_oka_dref="reference_diameter_dref",
        dpm_bc_erosion_oka_e90="reference_erosion_rate_e90",
        dpm_bc_erosion_oka_hv="wall_vickers_hardness_hv",
        dpm_bc_erosion_oka_k2="velocity_exponent_k2",
        dpm_bc_erosion_oka_k3="diameter_exponent_k3",
        dpm_bc_erosion_oka_n1="model_constant_n1",
        dpm_bc_erosion_oka_n2="model_constant_n2",
        dpm_bc_erosion_oka_vref="reference_velocity_vref",
        dpm_bc_erosion_oka="enabled",
    )

