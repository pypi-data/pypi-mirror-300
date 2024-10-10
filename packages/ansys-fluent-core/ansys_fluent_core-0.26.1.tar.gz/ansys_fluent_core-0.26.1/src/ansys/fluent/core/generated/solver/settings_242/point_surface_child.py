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
from .reference_frame_10 import reference_frame as reference_frame_cls
from .coordinate import coordinate as coordinate_cls
from .point_1 import point as point_cls
from .r_1 import r as r_cls
from .theta_1 import theta as theta_cls
from .z_5 import z as z_cls
from .snap_method import snap_method as snap_method_cls
from .dynamic import dynamic as dynamic_cls
from .display_4 import display as display_cls

class point_surface_child(Group):
    """
    'child_object_type' of point_surface.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'reference_frame', 'coordinate', 'point', 'r', 'theta', 'z',
         'snap_method', 'dynamic']

    command_names = \
        ['display']

    _child_classes = dict(
        name=name_cls,
        reference_frame=reference_frame_cls,
        coordinate=coordinate_cls,
        point=point_cls,
        r=r_cls,
        theta=theta_cls,
        z=z_cls,
        snap_method=snap_method_cls,
        dynamic=dynamic_cls,
        display=display_cls,
    )

