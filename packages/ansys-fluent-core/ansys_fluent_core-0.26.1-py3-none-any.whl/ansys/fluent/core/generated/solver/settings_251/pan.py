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

from .right import right as right_cls
from .up import up as up_cls

class pan(Command):
    """
    Adjust the camera position without modifying the position.
    
    Parameters
    ----------
        right : real
            'right' child.
        up : real
            'up' child.
    
    """

    fluent_name = "pan"

    argument_names = \
        ['right', 'up']

    _child_classes = dict(
        right=right_cls,
        up=up_cls,
    )

