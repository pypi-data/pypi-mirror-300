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

from .width_1 import width as width_cls
from .height import height as height_cls

class field(Command):
    """
    Set the field of view (width and height).
    
    Parameters
    ----------
        width : real
            'width' child.
        height : real
            'height' child.
    
    """

    fluent_name = "field"

    argument_names = \
        ['width', 'height']

    _child_classes = dict(
        width=width_cls,
        height=height_cls,
    )

