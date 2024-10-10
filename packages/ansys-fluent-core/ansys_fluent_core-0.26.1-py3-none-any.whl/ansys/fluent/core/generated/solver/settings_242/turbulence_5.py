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

from .les_spec import les_spec as les_spec_cls
from .fluctuating_velocity_algorithm import fluctuating_velocity_algorithm as fluctuating_velocity_algorithm_cls
from .number_of_fourier_modes import number_of_fourier_modes as number_of_fourier_modes_cls
from .number_of_vortices import number_of_vortices as number_of_vortices_cls
from .streamwise_fluctuations import streamwise_fluctuations as streamwise_fluctuations_cls
from .satisfy_mass_conservation import satisfy_mass_conservation as satisfy_mass_conservation_cls
from .scale_search_limiter import scale_search_limiter as scale_search_limiter_cls
from .stg_turbulent_intensity import stg_turbulent_intensity as stg_turbulent_intensity_cls
from .stg_turbulent_viscosity_ratio import stg_turbulent_viscosity_ratio as stg_turbulent_viscosity_ratio_cls
from .wall_distance import wall_distance as wall_distance_cls
from .volumetric_forcing import volumetric_forcing as volumetric_forcing_cls
from .forcing_zone_thickness import forcing_zone_thickness as forcing_zone_thickness_cls
from .volumetric_thickness import volumetric_thickness as volumetric_thickness_cls
from .turbulence_specification import turbulence_specification as turbulence_specification_cls
from .modified_turbulent_viscosity import modified_turbulent_viscosity as modified_turbulent_viscosity_cls
from .laminar_kinetic_energy import laminar_kinetic_energy as laminar_kinetic_energy_cls
from .intermittency import intermittency as intermittency_cls
from .turbulent_kinetic_energy import turbulent_kinetic_energy as turbulent_kinetic_energy_cls
from .turbulent_dissipation_rate import turbulent_dissipation_rate as turbulent_dissipation_rate_cls
from .specific_dissipation_rate import specific_dissipation_rate as specific_dissipation_rate_cls
from .velocity_variance_scale import velocity_variance_scale as velocity_variance_scale_cls
from .turbulent_intensity import turbulent_intensity as turbulent_intensity_cls
from .turbulent_length_scale import turbulent_length_scale as turbulent_length_scale_cls
from .hydraulic_diameter import hydraulic_diameter as hydraulic_diameter_cls
from .turbulent_viscosity_ratio import turbulent_viscosity_ratio as turbulent_viscosity_ratio_cls
from .turbulent_viscosity_ratio_profile import turbulent_viscosity_ratio_profile as turbulent_viscosity_ratio_profile_cls
from .reynolds_stress_specification import reynolds_stress_specification as reynolds_stress_specification_cls
from .uu_reynolds_stresses import uu_reynolds_stresses as uu_reynolds_stresses_cls
from .vv_reynolds_stresses import vv_reynolds_stresses as vv_reynolds_stresses_cls
from .ww_reynolds_stresses import ww_reynolds_stresses as ww_reynolds_stresses_cls
from .uv_reynolds_stresses import uv_reynolds_stresses as uv_reynolds_stresses_cls
from .vw_reynolds_stresses import vw_reynolds_stresses as vw_reynolds_stresses_cls
from .uw_reynolds_stresses import uw_reynolds_stresses as uw_reynolds_stresses_cls
from .subgrid_kinetic_energy_specification import subgrid_kinetic_energy_specification as subgrid_kinetic_energy_specification_cls
from .subgrid_kinetic_energy import subgrid_kinetic_energy as subgrid_kinetic_energy_cls
from .subgrid_turbulent_intensity import subgrid_turbulent_intensity as subgrid_turbulent_intensity_cls

class turbulence(Group):
    """
    Help not available.
    """

    fluent_name = "turbulence"

    child_names = \
        ['les_spec', 'fluctuating_velocity_algorithm',
         'number_of_fourier_modes', 'number_of_vortices',
         'streamwise_fluctuations', 'satisfy_mass_conservation',
         'scale_search_limiter', 'stg_turbulent_intensity',
         'stg_turbulent_viscosity_ratio', 'wall_distance',
         'volumetric_forcing', 'forcing_zone_thickness',
         'volumetric_thickness', 'turbulence_specification',
         'modified_turbulent_viscosity', 'laminar_kinetic_energy',
         'intermittency', 'turbulent_kinetic_energy',
         'turbulent_dissipation_rate', 'specific_dissipation_rate',
         'velocity_variance_scale', 'turbulent_intensity',
         'turbulent_length_scale', 'hydraulic_diameter',
         'turbulent_viscosity_ratio', 'turbulent_viscosity_ratio_profile',
         'reynolds_stress_specification', 'uu_reynolds_stresses',
         'vv_reynolds_stresses', 'ww_reynolds_stresses',
         'uv_reynolds_stresses', 'vw_reynolds_stresses',
         'uw_reynolds_stresses', 'subgrid_kinetic_energy_specification',
         'subgrid_kinetic_energy', 'subgrid_turbulent_intensity']

    _child_classes = dict(
        les_spec=les_spec_cls,
        fluctuating_velocity_algorithm=fluctuating_velocity_algorithm_cls,
        number_of_fourier_modes=number_of_fourier_modes_cls,
        number_of_vortices=number_of_vortices_cls,
        streamwise_fluctuations=streamwise_fluctuations_cls,
        satisfy_mass_conservation=satisfy_mass_conservation_cls,
        scale_search_limiter=scale_search_limiter_cls,
        stg_turbulent_intensity=stg_turbulent_intensity_cls,
        stg_turbulent_viscosity_ratio=stg_turbulent_viscosity_ratio_cls,
        wall_distance=wall_distance_cls,
        volumetric_forcing=volumetric_forcing_cls,
        forcing_zone_thickness=forcing_zone_thickness_cls,
        volumetric_thickness=volumetric_thickness_cls,
        turbulence_specification=turbulence_specification_cls,
        modified_turbulent_viscosity=modified_turbulent_viscosity_cls,
        laminar_kinetic_energy=laminar_kinetic_energy_cls,
        intermittency=intermittency_cls,
        turbulent_kinetic_energy=turbulent_kinetic_energy_cls,
        turbulent_dissipation_rate=turbulent_dissipation_rate_cls,
        specific_dissipation_rate=specific_dissipation_rate_cls,
        velocity_variance_scale=velocity_variance_scale_cls,
        turbulent_intensity=turbulent_intensity_cls,
        turbulent_length_scale=turbulent_length_scale_cls,
        hydraulic_diameter=hydraulic_diameter_cls,
        turbulent_viscosity_ratio=turbulent_viscosity_ratio_cls,
        turbulent_viscosity_ratio_profile=turbulent_viscosity_ratio_profile_cls,
        reynolds_stress_specification=reynolds_stress_specification_cls,
        uu_reynolds_stresses=uu_reynolds_stresses_cls,
        vv_reynolds_stresses=vv_reynolds_stresses_cls,
        ww_reynolds_stresses=ww_reynolds_stresses_cls,
        uv_reynolds_stresses=uv_reynolds_stresses_cls,
        vw_reynolds_stresses=vw_reynolds_stresses_cls,
        uw_reynolds_stresses=uw_reynolds_stresses_cls,
        subgrid_kinetic_energy_specification=subgrid_kinetic_energy_specification_cls,
        subgrid_kinetic_energy=subgrid_kinetic_energy_cls,
        subgrid_turbulent_intensity=subgrid_turbulent_intensity_cls,
    )

    _child_aliases = dict(
        e="turbulent_dissipation_rate",
        intermit="intermittency",
        k="turbulent_kinetic_energy",
        kl="laminar_kinetic_energy",
        ksgs="subgrid_kinetic_energy",
        ksgs_spec="subgrid_kinetic_energy_specification",
        nut="modified_turbulent_viscosity",
        o="specific_dissipation_rate",
        rfg_number_of_modes="number_of_fourier_modes",
        rst_spec="reynolds_stress_specification",
        sgs_turb_intensity="subgrid_turbulent_intensity",
        stg_dw_limiter="wall_distance",
        stg_scale_limiter_type="scale_search_limiter",
        stg_ti_limiter="stg_turbulent_intensity",
        stg_tvr_limiter="stg_turbulent_viscosity_ratio",
        turb_hydraulic_diam="hydraulic_diameter",
        turb_intensity="turbulent_intensity",
        turb_length_scale="turbulent_length_scale",
        turb_viscosity_ratio="turbulent_viscosity_ratio",
        turb_viscosity_ratio_profile="turbulent_viscosity_ratio_profile",
        turbulent_specification="turbulence_specification",
        uu="uu_reynolds_stresses",
        uv="uv_reynolds_stresses",
        uw="uw_reynolds_stresses",
        v2="velocity_variance_scale",
        vm_mass_conservation="satisfy_mass_conservation",
        vm_number_of_vortices="number_of_vortices",
        vm_streamwise_fluct="streamwise_fluctuations",
        volumetric_synthetic_turbulence_generator_option="forcing_zone_thickness",
        volumetric_synthetic_turbulence_generator_option_thickness="volumetric_thickness",
        volumetric_synthetic_turbulence_generator="volumetric_forcing",
        vv="vv_reynolds_stresses",
        vw="vw_reynolds_stresses",
        ww="ww_reynolds_stresses",
    )

