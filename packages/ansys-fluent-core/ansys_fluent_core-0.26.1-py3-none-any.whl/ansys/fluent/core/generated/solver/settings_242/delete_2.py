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

from .name_3 import name as name_cls

class delete(CommandWithPositionalArgs):
    """
    Delete a mesh interface.
    
    Parameters
    ----------
        name : str
            Mesh interface name to be deleted.
    
    """

    fluent_name = "delete"

    argument_names = \
        ['name']

    _child_classes = dict(
        name=name_cls,
    )

