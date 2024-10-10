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

from .display_12 import display as display_cls

class display(Command):
    """
    Transient display.
    
    Parameters
    ----------
        display : str
            Select graphics object name for transient display.
    
    """

    fluent_name = "display"

    argument_names = \
        ['display']

    _child_classes = dict(
        display=display_cls,
    )

