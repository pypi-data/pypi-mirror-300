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

from .address import address as address_cls
from .port import port as port_cls

class start(Command):
    """
    'start' command.
    
    Parameters
    ----------
        address : str
            'address' child.
        port : int
            'port' child.
    
    """

    fluent_name = "start"

    argument_names = \
        ['address', 'port']

    _child_classes = dict(
        address=address_cls,
        port=port_cls,
    )

    return_type = "<object object at 0x7ff9d2a0f590>"
