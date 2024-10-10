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

from .bc_type_2 import bc_type as bc_type_cls
from .particle_wall_heat_exchange_enabled import particle_wall_heat_exchange_enabled as particle_wall_heat_exchange_enabled_cls
from .reflection_coefficients import reflection_coefficients as reflection_coefficients_cls
from .dem_collision_partner import dem_collision_partner as dem_collision_partner_cls
from .reinject_using_injection import reinject_using_injection as reinject_using_injection_cls
from .bc_user_function import bc_user_function as bc_user_function_cls
from .film_condensation_enabled import film_condensation_enabled as film_condensation_enabled_cls
from .gas_side_boundary_layer_model_enabled import gas_side_boundary_layer_model_enabled as gas_side_boundary_layer_model_enabled_cls
from .lwf_to_vof_enabled import lwf_to_vof_enabled as lwf_to_vof_enabled_cls
from .vof_to_lwf_enabled import vof_to_lwf_enabled as vof_to_lwf_enabled_cls
from .impingement_splashing import impingement_splashing as impingement_splashing_cls
from .wall_roughness_parameters import wall_roughness_parameters as wall_roughness_parameters_cls
from .friction_coefficient import friction_coefficient as friction_coefficient_cls
from .film_separation import film_separation as film_separation_cls
from .film_particle_stripping import film_particle_stripping as film_particle_stripping_cls
from .film_initialization import film_initialization as film_initialization_cls
from .film_in_situ_data_reduction import film_in_situ_data_reduction as film_in_situ_data_reduction_cls
from .erosion import erosion as erosion_cls

class discrete_phase(Group):
    """
    Allows to change DPM model variables or settings.
    """

    fluent_name = "discrete-phase"

    child_names = \
        ['bc_type', 'particle_wall_heat_exchange_enabled',
         'reflection_coefficients', 'dem_collision_partner',
         'reinject_using_injection', 'bc_user_function',
         'film_condensation_enabled', 'gas_side_boundary_layer_model_enabled',
         'lwf_to_vof_enabled', 'vof_to_lwf_enabled', 'impingement_splashing',
         'wall_roughness_parameters', 'friction_coefficient',
         'film_separation', 'film_particle_stripping', 'film_initialization',
         'film_in_situ_data_reduction', 'erosion']

    _child_classes = dict(
        bc_type=bc_type_cls,
        particle_wall_heat_exchange_enabled=particle_wall_heat_exchange_enabled_cls,
        reflection_coefficients=reflection_coefficients_cls,
        dem_collision_partner=dem_collision_partner_cls,
        reinject_using_injection=reinject_using_injection_cls,
        bc_user_function=bc_user_function_cls,
        film_condensation_enabled=film_condensation_enabled_cls,
        gas_side_boundary_layer_model_enabled=gas_side_boundary_layer_model_enabled_cls,
        lwf_to_vof_enabled=lwf_to_vof_enabled_cls,
        vof_to_lwf_enabled=vof_to_lwf_enabled_cls,
        impingement_splashing=impingement_splashing_cls,
        wall_roughness_parameters=wall_roughness_parameters_cls,
        friction_coefficient=friction_coefficient_cls,
        film_separation=film_separation_cls,
        film_particle_stripping=film_particle_stripping_cls,
        film_initialization=film_initialization_cls,
        film_in_situ_data_reduction=film_in_situ_data_reduction_cls,
        erosion=erosion_cls,
    )

    _child_aliases = dict(
        data_reduction="film_in_situ_data_reduction",
        discrete_phase_bc_function="bc_user_function",
        discrete_phase_bc_type="bc_type",
        dpm_allow_lwf_to_vof="lwf_to_vof_enabled",
        dpm_allow_vof_to_lwf="vof_to_lwf_enabled",
        dpm_bc_erosion_dnv_ductile="erosion/dnv/ductile_material_enabled",
        dpm_bc_erosion_dnv_k="erosion/dnv/model_constant_k",
        dpm_bc_erosion_dnv_n="erosion/dnv/model_constant_n",
        dpm_bc_erosion_dnv="erosion/dnv/enabled",
        dpm_bc_erosion_finnie_k="erosion/finnie/model_constant_k",
        dpm_bc_erosion_finnie_max_erosion_angle="erosion/finnie/angle_of_max_erosion",
        dpm_bc_erosion_finnie_vel_exp="erosion/finnie/velocity_exponent",
        dpm_bc_erosion_mclaury_a="erosion/mclaury/model_constant_a",
        dpm_bc_erosion_mclaury_b="erosion/mclaury/impact_angle_constant_b",
        dpm_bc_erosion_mclaury_c="erosion/mclaury/impact_angle_constant_c",
        dpm_bc_erosion_mclaury_transition_angle="erosion/mclaury/transition_angle",
        dpm_bc_erosion_mclaury_vel_exp="erosion/mclaury/velocity_exponent",
        dpm_bc_erosion_mclaury_w="erosion/mclaury/impact_angle_constant_w",
        dpm_bc_erosion_mclaury_x="erosion/mclaury/impact_angle_constant_x",
        dpm_bc_erosion_mclaury_y="erosion/mclaury/impact_angle_constant_y",
        dpm_bc_erosion_mclaury="erosion/mclaury/enabled",
        dpm_bc_erosion_oka_dref="erosion/oka/reference_diameter_dref",
        dpm_bc_erosion_oka_e90="erosion/oka/reference_erosion_rate_e90",
        dpm_bc_erosion_oka_hv="erosion/oka/wall_vickers_hardness_hv",
        dpm_bc_erosion_oka_k2="erosion/oka/velocity_exponent_k2",
        dpm_bc_erosion_oka_k3="erosion/oka/diameter_exponent_k3",
        dpm_bc_erosion_oka_n1="erosion/oka/model_constant_n1",
        dpm_bc_erosion_oka_n2="erosion/oka/model_constant_n2",
        dpm_bc_erosion_oka_vref="erosion/oka/reference_velocity_vref",
        dpm_bc_erosion_oka="erosion/oka/enabled",
        dpm_bc_erosion_shear_c="erosion/shear_erosion/model_constant_c",
        dpm_bc_erosion_shear_packing_limit="erosion/shear_erosion/packing_limit",
        dpm_bc_erosion_shear_v="erosion/shear_erosion/velocity_exponent_v",
        dpm_bc_erosion_shear="erosion/shear_erosion/enabled",
        dpm_bc_erosion_shielding="erosion/shear_erosion/shielding_enabled",
        dpm_bc_frictn_coeff="friction_coefficient",
        dpm_bc_norm_coeff="reflection_coefficients/normal",
        dpm_bc_tang_coeff="reflection_coefficients/tangential",
        dpm_calibratable_temp="impingement_splashing/regime_parameters/critical_temperature_offset",
        dpm_crit_temp_option="impingement_splashing/regime_parameters/critical_temperature_option",
        dpm_critical_shear_stress="film_particle_stripping/critical_shear_stress",
        dpm_critical_temp_factor="impingement_splashing/regime_parameters/critical_temperature_factor",
        dpm_critical_we_number="film_separation/critical_weber_number",
        dpm_deposition_delta_t="impingement_splashing/regime_parameters/deposition_delta_t",
        dpm_do_initialize_lwf_now="film_initialization/do_initialization_now",
        dpm_film_bl_model="gas_side_boundary_layer_model_enabled",
        dpm_film_condensation="film_condensation_enabled",
        dpm_film_separation_angle="film_separation/separation_angle",
        dpm_film_separation_model="film_separation/model",
        dpm_film_splash_nsamp="impingement_splashing/number_of_splashed_drops",
        dpm_impingement_splashing_model="impingement_splashing/model",
        dpm_initial_height="film_initialization/film_height",
        dpm_initial_injection="film_initialization/injection",
        dpm_initial_temperature="film_initialization/film_temperature",
        dpm_initialize_lwf="film_initialization/enabled",
        dpm_laplace_number_constant="impingement_splashing/regime_parameters/laplace_number_constant",
        dpm_partial_evaporation_ratio="impingement_splashing/regime_parameters/partial_evaporation_ratio",
        dpm_particle_stripping="film_particle_stripping/enabled",
        dpm_upper_deposition_limit_offset="impingement_splashing/regime_parameters/upper_deposition_limit_offset",
        dpm_wall_heat_exchange="particle_wall_heat_exchange_enabled",
        dpm_bc_collision_partner="dem_collision_partner",
        dpm_bc_type="bc_type",
        dpm_bc_udf="bc_user_function",
        enable_finnie_erosion_model="erosion/finnie/enabled",
        enable_generic_erosion_model="erosion/generic/enabled",
        film_parcel_surface_area_density="film_initialization/min_parcels_per_facet",
        film_velocity="film_initialization/film_velocity",
        generic_diameter_function="erosion/generic/diameter_function",
        generic_impact_angle_function="erosion/generic/impact_angle_function",
        generic_velocity_exponent_function="erosion/generic/velocity_exponent_function",
        in_situ_data_reduction="film_in_situ_data_reduction/enabled",
        initialize_lwf_now="film_initialization/do_initialization_now",
        minimum_number_of_parcels_per_face="film_initialization/min_parcels_per_unit_area",
        normal_coefficient="reflection_coefficients/normal",
        ra_roughness="wall_roughness_parameters/ra",
        reinj_inj="reinject_using_injection",
        rq_roughness="wall_roughness_parameters/rq",
        rsm_roughness="wall_roughness_parameters/rsm",
        rz_roughness="wall_roughness_parameters/rz",
        tangential_coefficient="reflection_coefficients/tangential",
    )

