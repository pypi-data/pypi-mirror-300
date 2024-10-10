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

from .copy_from import copy_from as copy_from_cls
from .copy_to import copy_to as copy_to_cls

class copy(Command):
    """
    'copy' command.
    
    Parameters
    ----------
        copy_from : str
            'copy_from' child.
        copy_to : str
            'copy_to' child.
    
    """

    fluent_name = "copy"

    argument_names = \
        ['copy_from', 'copy_to']

    _child_classes = dict(
        copy_from=copy_from_cls,
        copy_to=copy_to_cls,
    )

    return_type = "<object object at 0x7fd93fabe420>"
