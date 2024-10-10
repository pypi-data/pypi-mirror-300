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

from .zone_names_1 import zone_names as zone_names_cls
from .scale import scale as scale_cls

class scale_zone(Command):
    """
    Scale nodal coordinates of input cell zones.
    
    Parameters
    ----------
        zone_names : List
            Scale specified cell zones.
        scale : List
            'scale' child.
    
    """

    fluent_name = "scale-zone"

    argument_names = \
        ['zone_names', 'scale']

    _child_classes = dict(
        zone_names=zone_names_cls,
        scale=scale_cls,
    )

