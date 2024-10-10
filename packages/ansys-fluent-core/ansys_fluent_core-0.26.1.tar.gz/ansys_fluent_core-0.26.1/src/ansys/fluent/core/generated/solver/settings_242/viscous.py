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

from .model_1 import model as model_cls
from .spalart_allmaras_production import spalart_allmaras_production as spalart_allmaras_production_cls
from .k_epsilon_model import k_epsilon_model as k_epsilon_model_cls
from .k_omega_model import k_omega_model as k_omega_model_cls
from .k_omega_options import k_omega_options as k_omega_options_cls
from .geko_options import geko_options as geko_options_cls
from .rng_options import rng_options as rng_options_cls
from .near_wall_treatment import near_wall_treatment as near_wall_treatment_cls
from .reynolds_stress_model import reynolds_stress_model as reynolds_stress_model_cls
from .subgrid_scale_model import subgrid_scale_model as subgrid_scale_model_cls
from .les_model_options import les_model_options as les_model_options_cls
from .reynolds_stress_options import reynolds_stress_options as reynolds_stress_options_cls
from .rans_model import rans_model as rans_model_cls
from .des_options import des_options as des_options_cls
from .transition_module import transition_module as transition_module_cls
from .hybrid_rans_les import hybrid_rans_les as hybrid_rans_les_cls
from .sbes_options import sbes_options as sbes_options_cls
from .user_defined_transition import user_defined_transition as user_defined_transition_cls
from .options_1 import options as options_cls
from .multiphase_turbulence import multiphase_turbulence as multiphase_turbulence_cls
from .turbulence_expert import turbulence_expert as turbulence_expert_cls
from .transition_model_options import transition_model_options as transition_model_options_cls
from .transition_sst_option import transition_sst_option as transition_sst_option_cls
from .user_defined_2 import user_defined as user_defined_cls
from .sa_enhanced_wall_treatment import sa_enhanced_wall_treatment as sa_enhanced_wall_treatment_cls
from .sa_damping import sa_damping as sa_damping_cls

class viscous(Group):
    """
    'viscous' child.
    """

    fluent_name = "viscous"

    child_names = \
        ['model', 'spalart_allmaras_production', 'k_epsilon_model',
         'k_omega_model', 'k_omega_options', 'geko_options', 'rng_options',
         'near_wall_treatment', 'reynolds_stress_model',
         'subgrid_scale_model', 'les_model_options',
         'reynolds_stress_options', 'rans_model', 'des_options',
         'transition_module', 'hybrid_rans_les', 'sbes_options',
         'user_defined_transition', 'options', 'multiphase_turbulence',
         'turbulence_expert', 'transition_model_options',
         'transition_sst_option', 'user_defined',
         'sa_enhanced_wall_treatment', 'sa_damping']

    _child_classes = dict(
        model=model_cls,
        spalart_allmaras_production=spalart_allmaras_production_cls,
        k_epsilon_model=k_epsilon_model_cls,
        k_omega_model=k_omega_model_cls,
        k_omega_options=k_omega_options_cls,
        geko_options=geko_options_cls,
        rng_options=rng_options_cls,
        near_wall_treatment=near_wall_treatment_cls,
        reynolds_stress_model=reynolds_stress_model_cls,
        subgrid_scale_model=subgrid_scale_model_cls,
        les_model_options=les_model_options_cls,
        reynolds_stress_options=reynolds_stress_options_cls,
        rans_model=rans_model_cls,
        des_options=des_options_cls,
        transition_module=transition_module_cls,
        hybrid_rans_les=hybrid_rans_les_cls,
        sbes_options=sbes_options_cls,
        user_defined_transition=user_defined_transition_cls,
        options=options_cls,
        multiphase_turbulence=multiphase_turbulence_cls,
        turbulence_expert=turbulence_expert_cls,
        transition_model_options=transition_model_options_cls,
        transition_sst_option=transition_sst_option_cls,
        user_defined=user_defined_cls,
        sa_enhanced_wall_treatment=sa_enhanced_wall_treatment_cls,
        sa_damping=sa_damping_cls,
    )

