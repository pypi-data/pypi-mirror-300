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

from .outlet_zone import outlet_zone as outlet_zone_cls
from .temperature_rise_specification import temperature_rise_specification as temperature_rise_specification_cls
from .temperature_rise import temperature_rise as temperature_rise_cls
from .heat_source import heat_source as heat_source_cls
from .freestream_temperature import freestream_temperature as freestream_temperature_cls
from .transfer_coefficient import transfer_coefficient as transfer_coefficient_cls
from .direction_specification import direction_specification as direction_specification_cls
from .coordinate_system_1 import coordinate_system as coordinate_system_cls
from .flow_direction import flow_direction as flow_direction_cls
from .direction_vector import direction_vector as direction_vector_cls
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
from .species_mass_fractions import species_mass_fractions as species_mass_fractions_cls
from .participates_in_solar_ray_tracing import participates_in_solar_ray_tracing as participates_in_solar_ray_tracing_cls
from .solar_transmissivity_factor import solar_transmissivity_factor as solar_transmissivity_factor_cls

class recirculation_inlet(Group):
    """
    Help not available.
    """

    fluent_name = "recirculation-inlet"

    child_names = \
        ['outlet_zone', 'temperature_rise_specification', 'temperature_rise',
         'heat_source', 'freestream_temperature', 'transfer_coefficient',
         'direction_specification', 'coordinate_system', 'flow_direction',
         'direction_vector', 'turbulence_specification',
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
         'subgrid_kinetic_energy', 'subgrid_turbulent_intensity',
         'species_mass_fractions', 'participates_in_solar_ray_tracing',
         'solar_transmissivity_factor']

    _child_classes = dict(
        outlet_zone=outlet_zone_cls,
        temperature_rise_specification=temperature_rise_specification_cls,
        temperature_rise=temperature_rise_cls,
        heat_source=heat_source_cls,
        freestream_temperature=freestream_temperature_cls,
        transfer_coefficient=transfer_coefficient_cls,
        direction_specification=direction_specification_cls,
        coordinate_system=coordinate_system_cls,
        flow_direction=flow_direction_cls,
        direction_vector=direction_vector_cls,
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
        species_mass_fractions=species_mass_fractions_cls,
        participates_in_solar_ray_tracing=participates_in_solar_ray_tracing_cls,
        solar_transmissivity_factor=solar_transmissivity_factor_cls,
    )

    _child_aliases = dict(
        direction_spec="direction_specification",
        direction_vector_components="direction_vector",
        e="turbulent_dissipation_rate",
        flow_direction_component="flow_direction",
        hc="transfer_coefficient",
        intermit="intermittency",
        k="turbulent_kinetic_energy",
        kl="laminar_kinetic_energy",
        ksgs="subgrid_kinetic_energy",
        ksgs_spec="subgrid_kinetic_energy_specification",
        mass_flow_multiplier="species_mass_fractions",
        nut="modified_turbulent_viscosity",
        o="specific_dissipation_rate",
        pid="outlet_zone",
        rst_spec="reynolds_stress_specification",
        sgs_turb_intensity="subgrid_turbulent_intensity",
        solar_fluxes="participates_in_solar_ray_tracing",
        solar_shining_factor="solar_transmissivity_factor",
        temperature_spec="temperature_rise_specification",
        tinf="freestream_temperature",
        turb_hydraulic_diam="hydraulic_diameter",
        turb_intensity="turbulent_intensity",
        turb_length_scale="turbulent_length_scale",
        turb_viscosity_ratio="turbulent_viscosity_ratio",
        turb_viscosity_ratio_profile="turbulent_viscosity_ratio_profile",
        uu="uu_reynolds_stresses",
        uv="uv_reynolds_stresses",
        uw="uw_reynolds_stresses",
        v2="velocity_variance_scale",
        vv="vv_reynolds_stresses",
        vw="vw_reynolds_stresses",
        ww="ww_reynolds_stresses",
    )

