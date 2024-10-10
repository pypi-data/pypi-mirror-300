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

from .zone_names_4 import zone_names as zone_names_cls

class create_multiple_zone_surfaces(Command):
    """
    Provides access to creating new and editing multiple zone surfaces.
    
    Parameters
    ----------
        zone_names : List
            Enter zone name list.
    
    """

    fluent_name = "create-multiple-zone-surfaces"

    argument_names = \
        ['zone_names']

    _child_classes = dict(
        zone_names=zone_names_cls,
    )

