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

from .name import name as name_cls
from .zones import zones as zones_cls

class replace(Command):
    """
    Replace mesh and interpolate data.
    
    Parameters
    ----------
        name : str
            'name' child.
        zones : bool
            'zones' child.
    
    """

    fluent_name = "replace"

    argument_names = \
        ['name', 'zones']

    _child_classes = dict(
        name=name_cls,
        zones=zones_cls,
    )

    return_type = "<object object at 0x7fe5bb5024b0>"
