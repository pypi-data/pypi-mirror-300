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

from .anisotropic_boundary_zones import anisotropic_boundary_zones as anisotropic_boundary_zones_cls
from .cell_zones import cell_zones as cell_zones_cls
from .dynamic_adaption_frequency import dynamic_adaption_frequency as dynamic_adaption_frequency_cls
from .verbosity import verbosity as verbosity_cls
from .encapsulate_children import encapsulate_children as encapsulate_children_cls
from .maximum_refinement_level import maximum_refinement_level as maximum_refinement_level_cls
from .minimum_cell_quality import minimum_cell_quality as minimum_cell_quality_cls
from .maximum_cell_count import maximum_cell_count as maximum_cell_count_cls
from .additional_refinement_layers import additional_refinement_layers as additional_refinement_layers_cls
from .anisotropic_adaption import anisotropic_adaption as anisotropic_adaption_cls
from .minimum_edge_length import minimum_edge_length as minimum_edge_length_cls
from .anisotropic_split_ratio import anisotropic_split_ratio as anisotropic_split_ratio_cls
from .overset_adapt_dead_cells import overset_adapt_dead_cells as overset_adapt_dead_cells_cls
from .dynamic_adaption import dynamic_adaption as dynamic_adaption_cls

class set(Group):
    fluent_name = ...
    child_names = ...
    anisotropic_boundary_zones: anisotropic_boundary_zones_cls = ...
    cell_zones: cell_zones_cls = ...
    dynamic_adaption_frequency: dynamic_adaption_frequency_cls = ...
    verbosity: verbosity_cls = ...
    encapsulate_children: encapsulate_children_cls = ...
    maximum_refinement_level: maximum_refinement_level_cls = ...
    minimum_cell_quality: minimum_cell_quality_cls = ...
    maximum_cell_count: maximum_cell_count_cls = ...
    additional_refinement_layers: additional_refinement_layers_cls = ...
    anisotropic_adaption: anisotropic_adaption_cls = ...
    minimum_edge_length: minimum_edge_length_cls = ...
    anisotropic_split_ratio: anisotropic_split_ratio_cls = ...
    overset_adapt_dead_cells: overset_adapt_dead_cells_cls = ...
    command_names = ...

    def dynamic_adaption(self, enable: bool):
        """
        Adapt the mesh during solution.
        
        Parameters
        ----------
            enable : bool
                'enable' child.
        
        """

    return_type = ...
