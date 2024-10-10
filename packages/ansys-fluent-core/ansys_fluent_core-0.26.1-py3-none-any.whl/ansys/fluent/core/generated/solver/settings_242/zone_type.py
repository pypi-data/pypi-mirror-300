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

from .zone_names_5 import zone_names as zone_names_cls
from .new_type import new_type as new_type_cls

class zone_type(Command):
    """
    Set a zone's type.
    
    Parameters
    ----------
        zone_names : List
            Enter zone id/name.
        new_type : str
            Give new zone type.
    
    """

    fluent_name = "zone-type"

    argument_names = \
        ['zone_names', 'new_type']

    _child_classes = dict(
        zone_names=zone_names_cls,
        new_type=new_type_cls,
    )

