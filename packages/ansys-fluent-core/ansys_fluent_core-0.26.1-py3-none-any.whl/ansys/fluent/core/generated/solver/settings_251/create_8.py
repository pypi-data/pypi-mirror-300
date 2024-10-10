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

from .name_20 import name as name_cls
from .surfaces_7 import surfaces as surfaces_cls

class create(CommandWithPositionalArgs):
    """
    Create a group of surfaces.
    
    Parameters
    ----------
        name : str
            Specify the name for the group surface.
        surfaces : List
            Specify the surfaces.
    
    """

    fluent_name = "create"

    argument_names = \
        ['name', 'surfaces']

    _child_classes = dict(
        name=name_cls,
        surfaces=surfaces_cls,
    )

