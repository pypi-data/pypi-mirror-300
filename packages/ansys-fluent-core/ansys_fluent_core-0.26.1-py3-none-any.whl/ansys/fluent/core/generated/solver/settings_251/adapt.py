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

from .refinement_criteria import refinement_criteria as refinement_criteria_cls
from .coarsening_criteria import coarsening_criteria as coarsening_criteria_cls
from .manual_refinement_criteria import manual_refinement_criteria as manual_refinement_criteria_cls
from .manual_coarsening_criteria import manual_coarsening_criteria as manual_coarsening_criteria_cls
from .set import set as set_cls
from .profile import profile as profile_cls
from .free_hierarchy import free_hierarchy as free_hierarchy_cls
from .multi_layer_refinement import multi_layer_refinement as multi_layer_refinement_cls
from .geometry import geometry as geometry_cls
from .adapt_mesh import adapt_mesh as adapt_mesh_cls
from .display_adaption_cells import display_adaption_cells as display_adaption_cells_cls
from .list_adaption_cells import list_adaption_cells as list_adaption_cells_cls

class adapt(Group):
    """
    Enter the adaption menu.
    """

    fluent_name = "adapt"

    child_names = \
        ['refinement_criteria', 'coarsening_criteria',
         'manual_refinement_criteria', 'manual_coarsening_criteria', 'set',
         'profile', 'free_hierarchy', 'multi_layer_refinement', 'geometry']

    command_names = \
        ['adapt_mesh', 'display_adaption_cells', 'list_adaption_cells']

    _child_classes = dict(
        refinement_criteria=refinement_criteria_cls,
        coarsening_criteria=coarsening_criteria_cls,
        manual_refinement_criteria=manual_refinement_criteria_cls,
        manual_coarsening_criteria=manual_coarsening_criteria_cls,
        set=set_cls,
        profile=profile_cls,
        free_hierarchy=free_hierarchy_cls,
        multi_layer_refinement=multi_layer_refinement_cls,
        geometry=geometry_cls,
        adapt_mesh=adapt_mesh_cls,
        display_adaption_cells=display_adaption_cells_cls,
        list_adaption_cells=list_adaption_cells_cls,
    )

