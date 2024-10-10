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

from .enabled_48 import enabled as enabled_cls
from .velocity_exponent_v import velocity_exponent_v as velocity_exponent_v_cls
from .model_constant_c import model_constant_c as model_constant_c_cls
from .packing_limit import packing_limit as packing_limit_cls
from .shielding_enabled import shielding_enabled as shielding_enabled_cls

class shear_erosion(Group):
    """
    Settings for the shear erosion model.
    """

    fluent_name = "shear-erosion"

    child_names = \
        ['enabled', 'velocity_exponent_v', 'model_constant_c',
         'packing_limit', 'shielding_enabled']

    _child_classes = dict(
        enabled=enabled_cls,
        velocity_exponent_v=velocity_exponent_v_cls,
        model_constant_c=model_constant_c_cls,
        packing_limit=packing_limit_cls,
        shielding_enabled=shielding_enabled_cls,
    )

    _child_aliases = dict(
        dpm_bc_erosion_shear_c="model_constant_c",
        dpm_bc_erosion_shear_packing_limit="packing_limit",
        dpm_bc_erosion_shear_v="velocity_exponent_v",
        dpm_bc_erosion_shear="enabled",
        dpm_bc_erosion_shielding="shielding_enabled",
    )

