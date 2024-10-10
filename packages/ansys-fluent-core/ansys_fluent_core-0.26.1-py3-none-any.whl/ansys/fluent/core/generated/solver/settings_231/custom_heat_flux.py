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

from .name import name as name_cls
from .wall_function import wall_function as wall_function_cls
from .surface_name_list import surface_name_list as surface_name_list_cls

class custom_heat_flux(Command):
    """
    Write a generic file for heat transfer.
    
    Parameters
    ----------
        name : str
            'name' child.
        wall_function : bool
            'wall_function' child.
        surface_name_list : List
            'surface_name_list' child.
    
    """

    fluent_name = "custom-heat-flux"

    argument_names = \
        ['name', 'wall_function', 'surface_name_list']

    _child_classes = dict(
        name=name_cls,
        wall_function=wall_function_cls,
        surface_name_list=surface_name_list_cls,
    )

    return_type = "<object object at 0x7ff9d2a0e740>"
