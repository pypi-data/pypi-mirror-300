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

from .cell_zone_list import cell_zone_list as cell_zone_list_cls

class activate_cell_zone(Command):
    """
    Activate a cell thread.
    
    Parameters
    ----------
        cell_zone_list : List
            Enter id/name of cell-zones to activate.
    
    """

    fluent_name = "activate-cell-zone"

    argument_names = \
        ['cell_zone_list']

    _child_classes = dict(
        cell_zone_list=cell_zone_list_cls,
    )

