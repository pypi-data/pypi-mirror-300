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

from .name_15 import name as name_cls
from .location_3 import location as location_cls

class split(Command):
    """
    Input boundary and location names to split.
    
    Parameters
    ----------
        name : str
            Input new boundary name.
        location : List
            Input location name which should be part of new boundary.
    
    """

    fluent_name = "split"

    argument_names = \
        ['name', 'location']

    _child_classes = dict(
        name=name_cls,
        location=location_cls,
    )

