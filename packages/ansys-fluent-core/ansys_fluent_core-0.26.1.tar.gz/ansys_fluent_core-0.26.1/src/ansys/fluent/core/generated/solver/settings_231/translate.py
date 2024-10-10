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

from .offset import offset as offset_cls

class translate(Command):
    """
    Translate the mesh.
    
    Parameters
    ----------
        offset : Tuple
            'offset' child.
    
    """

    fluent_name = "translate"

    argument_names = \
        ['offset']

    _child_classes = dict(
        offset=offset_cls,
    )

    return_type = "<object object at 0x7ff9d2a0f5c0>"
