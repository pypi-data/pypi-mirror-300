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

from .mesh_interface_name import mesh_interface_name as mesh_interface_name_cls
from .adjacent_cell_zone_1 import adjacent_cell_zone_1 as adjacent_cell_zone_1_cls
from .zone1_2 import zone1 as zone1_cls
from .adjacent_cell_zone_2 import adjacent_cell_zone_2 as adjacent_cell_zone_2_cls
from .zone2_2 import zone2 as zone2_cls
from .paired_zones import paired_zones as paired_zones_cls
from .turbo_choice_1 import turbo_choice as turbo_choice_cls
from .turbo_non_overlap_1 import turbo_non_overlap as turbo_non_overlap_cls

class create(CommandWithPositionalArgs):
    """
    Create turbo mesh interface.
    
    Parameters
    ----------
        mesh_interface_name : str
            Enter a mesh interface names.
        adjacent_cell_zone_1 : str
            Select adjacent cell zone 1.
        zone1 : str
            Select first interface defining this mesh-interface.
        adjacent_cell_zone_2 : str
            Select adjacent cell zone 2.
        zone2 : str
            Select second interface defining this mesh-interface.
        paired_zones : List
            Paired zones list.
        turbo_choice : str
            Enter your choice of pitch-change types.
        turbo_non_overlap : bool
            Enable non-overlapping walls option for this mesh-interface.
    
    """

    fluent_name = "create"

    argument_names = \
        ['mesh_interface_name', 'adjacent_cell_zone_1', 'zone1',
         'adjacent_cell_zone_2', 'zone2', 'paired_zones', 'turbo_choice',
         'turbo_non_overlap']

    _child_classes = dict(
        mesh_interface_name=mesh_interface_name_cls,
        adjacent_cell_zone_1=adjacent_cell_zone_1_cls,
        zone1=zone1_cls,
        adjacent_cell_zone_2=adjacent_cell_zone_2_cls,
        zone2=zone2_cls,
        paired_zones=paired_zones_cls,
        turbo_choice=turbo_choice_cls,
        turbo_non_overlap=turbo_non_overlap_cls,
    )

