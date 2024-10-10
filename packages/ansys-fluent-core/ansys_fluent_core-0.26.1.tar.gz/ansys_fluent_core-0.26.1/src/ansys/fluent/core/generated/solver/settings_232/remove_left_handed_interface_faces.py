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

from .enable_9 import enable as enable_cls
from .update_1 import update as update_cls

class remove_left_handed_interface_faces(Command):
    """
    Remove left-handed faces during mesh interface creation.
    
    Parameters
    ----------
        enable : bool
            Remove left-handed faces on mesh interfaces.
        update : bool
            'update' child.
    
    """

    fluent_name = "remove-left-handed-interface-faces?"

    argument_names = \
        ['enable', 'update']

    _child_classes = dict(
        enable=enable_cls,
        update=update_cls,
    )

    return_type = "<object object at 0x7fe5b915e3e0>"
