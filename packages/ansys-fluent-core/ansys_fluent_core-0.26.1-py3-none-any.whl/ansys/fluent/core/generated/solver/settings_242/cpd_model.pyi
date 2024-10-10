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

from .initial_fraction_of_bridges_in_coal_lattice import initial_fraction_of_bridges_in_coal_lattice as initial_fraction_of_bridges_in_coal_lattice_cls
from .initial_fraction_of_char_bridges import initial_fraction_of_char_bridges as initial_fraction_of_char_bridges_cls
from .lattice_coordination_number import lattice_coordination_number as lattice_coordination_number_cls
from .cluster_molecular_weight import cluster_molecular_weight as cluster_molecular_weight_cls
from .side_chain_molecular_weight import side_chain_molecular_weight as side_chain_molecular_weight_cls

class cpd_model(Group):
    fluent_name = ...
    child_names = ...
    initial_fraction_of_bridges_in_coal_lattice: initial_fraction_of_bridges_in_coal_lattice_cls = ...
    initial_fraction_of_char_bridges: initial_fraction_of_char_bridges_cls = ...
    lattice_coordination_number: lattice_coordination_number_cls = ...
    cluster_molecular_weight: cluster_molecular_weight_cls = ...
    side_chain_molecular_weight: side_chain_molecular_weight_cls = ...
