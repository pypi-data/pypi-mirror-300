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

from typing import Union, List, Tuple

from .half_angle import half_angle as half_angle_cls
from .dispersion_angle import dispersion_angle as dispersion_angle_cls
from .inner_radius import inner_radius as inner_radius_cls
from .outer_radius import outer_radius as outer_radius_cls
from .x_axis import x_axis as x_axis_cls
from .y_axis import y_axis as y_axis_cls
from .z_axis import z_axis as z_axis_cls

class cone_settings(Group):
    fluent_name = ...
    child_names = ...
    half_angle: half_angle_cls = ...
    dispersion_angle: dispersion_angle_cls = ...
    inner_radius: inner_radius_cls = ...
    outer_radius: outer_radius_cls = ...
    x_axis: x_axis_cls = ...
    y_axis: y_axis_cls = ...
    z_axis: z_axis_cls = ...
    return_type = ...
