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

from .periodic_method import periodic_method as periodic_method_cls
from .interface_name import interface_name as interface_name_cls
from .zone_name_4 import zone_name as zone_name_cls
from .shadow_zone_name import shadow_zone_name as shadow_zone_name_cls
from .rotate_periodic_1 import rotate_periodic as rotate_periodic_cls
from .new_origin import new_origin as new_origin_cls
from .origin_2 import origin as origin_cls
from .new_direction import new_direction as new_direction_cls
from .direction_1 import direction as direction_cls
from .auto_offset import auto_offset as auto_offset_cls
from .angle_offset import angle_offset as angle_offset_cls
from .trans_offset import trans_offset as trans_offset_cls
from .create_periodic import create_periodic as create_periodic_cls
from .create_matching import create_matching as create_matching_cls

class create_periodic_interface(Command):
    """
    Create a conformal or non-conformal periodic interface.
    
    Parameters
    ----------
        periodic_method : str
            Method for creating periodic boundary.
        interface_name : str
            Enter a name for this periodic interface.
        zone_name : str
            Enter id/name of zone to convert to periodic.
        shadow_zone_name : str
            Enter id/name of zone to convert to shadow.
        rotate_periodic : bool
            Rotational or tranlational periodic boundary.
        new_origin : bool
            Use a new origin instead of the default origin.
        origin : List
            User specified origin of rotation.
        new_direction : bool
            Use a new rotational axis/direction instead of the default one.
        direction : List
            User specified axis/direction of rotation.
        auto_offset : bool
            Automatically calculate periodic offset.
        angle_offset : real
            Angle of rotation.
        trans_offset : List
            Translation offset vector.
        create_periodic : bool
            Create periodic boundary.
        create_matching : bool
            Create matching interface.
    
    """

    fluent_name = "create-periodic-interface"

    argument_names = \
        ['periodic_method', 'interface_name', 'zone_name', 'shadow_zone_name',
         'rotate_periodic', 'new_origin', 'origin', 'new_direction',
         'direction', 'auto_offset', 'angle_offset', 'trans_offset',
         'create_periodic', 'create_matching']

    _child_classes = dict(
        periodic_method=periodic_method_cls,
        interface_name=interface_name_cls,
        zone_name=zone_name_cls,
        shadow_zone_name=shadow_zone_name_cls,
        rotate_periodic=rotate_periodic_cls,
        new_origin=new_origin_cls,
        origin=origin_cls,
        new_direction=new_direction_cls,
        direction=direction_cls,
        auto_offset=auto_offset_cls,
        angle_offset=angle_offset_cls,
        trans_offset=trans_offset_cls,
        create_periodic=create_periodic_cls,
        create_matching=create_matching_cls,
    )

