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

from .surface_3 import surface as surface_cls
from .priority import priority as priority_cls

class set_rendering_priority(Command):
    """
    'set_rendering_priority' command.
    
    Parameters
    ----------
        surface : str
            Select surface.
        priority : str
            Select surface.
    
    """

    fluent_name = "set-rendering-priority"

    argument_names = \
        ['surface', 'priority']

    _child_classes = dict(
        surface=surface_cls,
        priority=priority_cls,
    )

    return_type = "<object object at 0x7fd93f9c2a20>"
