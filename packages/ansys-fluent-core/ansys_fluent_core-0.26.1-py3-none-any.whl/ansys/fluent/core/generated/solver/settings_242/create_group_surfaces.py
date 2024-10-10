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

from .surfaces_8 import surfaces as surfaces_cls
from .name_11 import name as name_cls

class create_group_surfaces(Command):
    """
    Create a group of surfaces.
    
    Parameters
    ----------
        surfaces : List
            Select list of surfaces.
        name : str
            Specify the name for the group surface.
    
    """

    fluent_name = "create-group-surfaces"

    argument_names = \
        ['surfaces', 'name']

    _child_classes = dict(
        surfaces=surfaces_cls,
        name=name_cls,
    )

