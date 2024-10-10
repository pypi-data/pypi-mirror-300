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

from .multi_level_grid import multi_level_grid as multi_level_grid_cls
from .residual_reduction_level import residual_reduction_level as residual_reduction_level_cls
from .cycle_count import cycle_count as cycle_count_cls

class customize_fmg_initialization(Command):
    """
    'customize_fmg_initialization' command.
    
    Parameters
    ----------
        multi_level_grid : int
            'multi_level_grid' child.
        residual_reduction_level : List
            'residual_reduction_level' child.
        cycle_count : List
            'cycle_count' child.
    
    """

    fluent_name = "customize-fmg-initialization"

    argument_names = \
        ['multi_level_grid', 'residual_reduction_level', 'cycle_count']

    _child_classes = dict(
        multi_level_grid=multi_level_grid_cls,
        residual_reduction_level=residual_reduction_level_cls,
        cycle_count=cycle_count_cls,
    )

    return_type = "<object object at 0x7ff9d0a62320>"
