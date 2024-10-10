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

from .object_name_1 import object_name as object_name_cls

class display(Command):
    """
    Display graphics object.
    
    Parameters
    ----------
        object_name : str
            'object_name' child.
    
    """

    fluent_name = "display"

    argument_names = \
        ['object_name']

    _child_classes = dict(
        object_name=object_name_cls,
    )

