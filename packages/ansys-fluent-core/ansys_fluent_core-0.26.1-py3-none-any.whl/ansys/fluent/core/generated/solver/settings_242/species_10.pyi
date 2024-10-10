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

from .react_1 import react as react_cls
from .partially_catalytic import partially_catalytic as partially_catalytic_cls
from .partially_catalytic_material import partially_catalytic_material as partially_catalytic_material_cls
from .partially_catalytic_recombination_coefficient_o import partially_catalytic_recombination_coefficient_o as partially_catalytic_recombination_coefficient_o_cls
from .partially_catalytic_recombination_coefficient_n import partially_catalytic_recombination_coefficient_n as partially_catalytic_recombination_coefficient_n_cls
from .partially_catalytic_recombination_model import partially_catalytic_recombination_model as partially_catalytic_recombination_model_cls
from .species_boundary_conditions import species_boundary_conditions as species_boundary_conditions_cls
from .species_mass_fraction_or_flux import species_mass_fraction_or_flux as species_mass_fraction_or_flux_cls
from .reaction_mechs_1 import reaction_mechs as reaction_mechs_cls
from .surf_washcoat_factor import surf_washcoat_factor as surf_washcoat_factor_cls
from .initial_deposition_height import initial_deposition_height as initial_deposition_height_cls
from .solid_species_density import solid_species_density as solid_species_density_cls

class species(Group):
    fluent_name = ...
    child_names = ...
    react: react_cls = ...
    partially_catalytic: partially_catalytic_cls = ...
    partially_catalytic_material: partially_catalytic_material_cls = ...
    partially_catalytic_recombination_coefficient_o: partially_catalytic_recombination_coefficient_o_cls = ...
    partially_catalytic_recombination_coefficient_n: partially_catalytic_recombination_coefficient_n_cls = ...
    partially_catalytic_recombination_model: partially_catalytic_recombination_model_cls = ...
    species_boundary_conditions: species_boundary_conditions_cls = ...
    species_mass_fraction_or_flux: species_mass_fraction_or_flux_cls = ...
    reaction_mechs: reaction_mechs_cls = ...
    surf_washcoat_factor: surf_washcoat_factor_cls = ...
    initial_deposition_height: initial_deposition_height_cls = ...
    solid_species_density: solid_species_density_cls = ...
