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

from .linearization import linearization as linearization_cls
from .implicit_momentum_coupling import implicit_momentum_coupling as implicit_momentum_coupling_cls
from .implicit_source_term_coupling import implicit_source_term_coupling as implicit_source_term_coupling_cls
from .linear_growth_of_dpm_source_terms import linear_growth_of_dpm_source_terms as linear_growth_of_dpm_source_terms_cls
from .reset_sources_at_timestep import reset_sources_at_timestep as reset_sources_at_timestep_cls

class source_terms(Group):
    fluent_name = ...
    child_names = ...
    linearization: linearization_cls = ...
    implicit_momentum_coupling: implicit_momentum_coupling_cls = ...
    implicit_source_term_coupling: implicit_source_term_coupling_cls = ...
    linear_growth_of_dpm_source_terms: linear_growth_of_dpm_source_terms_cls = ...
    reset_sources_at_timestep: reset_sources_at_timestep_cls = ...
    return_type = ...
