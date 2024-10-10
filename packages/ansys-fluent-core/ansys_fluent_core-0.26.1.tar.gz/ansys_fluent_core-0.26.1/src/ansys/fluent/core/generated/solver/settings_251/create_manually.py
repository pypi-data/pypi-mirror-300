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

from .name_9 import name as name_cls
from .zone_list_1 import zone_list_1 as zone_list_1_cls
from .zone_list_2 import zone_list_2 as zone_list_2_cls
from .matching import matching as matching_cls
from .ignore_area_difference import ignore_area_difference as ignore_area_difference_cls

class create_manually(Command):
    """
    Create one-to-one interfaces between two groups of boundary zones even if they do not currently overlap.
    
    Parameters
    ----------
        name : str
            Enter a prefix for mesh interface names.
        zone_list_1 : List
            Enter the boundary zones belonging to the first group.
        zone_list_2 : List
            Enter the boundary zones belonging to the second group.
        matching : bool
            Indicate if mesh-interface is matching.
        ignore_area_difference : bool
            Check if user want to create poorly matched interface.
    
    """

    fluent_name = "create-manually"

    argument_names = \
        ['name', 'zone_list_1', 'zone_list_2', 'matching',
         'ignore_area_difference']

    _child_classes = dict(
        name=name_cls,
        zone_list_1=zone_list_1_cls,
        zone_list_2=zone_list_2_cls,
        matching=matching_cls,
        ignore_area_difference=ignore_area_difference_cls,
    )

