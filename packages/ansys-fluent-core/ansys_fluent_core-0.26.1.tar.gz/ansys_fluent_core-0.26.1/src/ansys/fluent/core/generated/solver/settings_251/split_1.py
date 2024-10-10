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

from .name_16 import name as name_cls
from .location_4 import location as location_cls

class split(Command):
    """
    Input volume and location names to split.
    
    Parameters
    ----------
        name : str
            Input new volume name.
        location : List
            Input location name which should be part of new volume.
    
    """

    fluent_name = "split"

    argument_names = \
        ['name', 'location']

    _child_classes = dict(
        name=name_cls,
        location=location_cls,
    )

