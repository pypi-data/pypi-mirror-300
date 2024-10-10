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

from .implicit_bodyforce_treatment import implicit_bodyforce_treatment as implicit_bodyforce_treatment_cls
from .velocity_formulation import velocity_formulation as velocity_formulation_cls
from .physical_velocity_formulation import physical_velocity_formulation as physical_velocity_formulation_cls
from .disable_rhie_chow_flux import disable_rhie_chow_flux as disable_rhie_chow_flux_cls
from .presto_pressure_scheme import presto_pressure_scheme as presto_pressure_scheme_cls
from .first_to_second_order_blending import first_to_second_order_blending as first_to_second_order_blending_cls
from .alternate_diffusion_for_porous_region_solids import alternate_diffusion_for_porous_region_solids as alternate_diffusion_for_porous_region_solids_cls

class numerics_pbns(Group):
    fluent_name = ...
    child_names = ...
    implicit_bodyforce_treatment: implicit_bodyforce_treatment_cls = ...
    velocity_formulation: velocity_formulation_cls = ...
    physical_velocity_formulation: physical_velocity_formulation_cls = ...
    disable_rhie_chow_flux: disable_rhie_chow_flux_cls = ...
    presto_pressure_scheme: presto_pressure_scheme_cls = ...
    first_to_second_order_blending: first_to_second_order_blending_cls = ...
    alternate_diffusion_for_porous_region_solids: alternate_diffusion_for_porous_region_solids_cls = ...
    return_type = ...
