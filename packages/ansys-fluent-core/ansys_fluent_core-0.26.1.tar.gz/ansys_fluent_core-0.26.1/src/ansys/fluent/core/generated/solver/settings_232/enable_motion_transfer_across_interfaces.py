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

from .enabled_2 import enabled as enabled_cls
from .option_name import option_name as option_name_cls

class enable_motion_transfer_across_interfaces(Command):
    """
    Transfer motion from one side of the interface to the other when only one side undergoes user-defined or system-coupling motion.
    
    Parameters
    ----------
        enabled : bool
            'enabled' child.
        option_name : str
            'option_name' child.
    
    """

    fluent_name = "enable-motion-transfer-across-interfaces"

    argument_names = \
        ['enabled', 'option_name']

    _child_classes = dict(
        enabled=enabled_cls,
        option_name=option_name_cls,
    )

    return_type = "<object object at 0x7fe5b915e390>"
