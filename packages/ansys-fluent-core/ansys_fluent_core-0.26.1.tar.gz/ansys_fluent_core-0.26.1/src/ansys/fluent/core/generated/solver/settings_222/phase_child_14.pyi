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

from .geom_disable import geom_disable as geom_disable_cls
from .geom_dir_spec import geom_dir_spec as geom_dir_spec_cls
from .geom_dir_x import geom_dir_x as geom_dir_x_cls
from .geom_dir_y import geom_dir_y as geom_dir_y_cls
from .geom_dir_z import geom_dir_z as geom_dir_z_cls
from .geom_levels import geom_levels as geom_levels_cls
from .geom_bgthread import geom_bgthread as geom_bgthread_cls
from .angular import angular as angular_cls
from .p_jump import p_jump as p_jump_cls

class phase_child(Group):
    fluent_name = ...
    child_names = ...
    geom_disable: geom_disable_cls = ...
    geom_dir_spec: geom_dir_spec_cls = ...
    geom_dir_x: geom_dir_x_cls = ...
    geom_dir_y: geom_dir_y_cls = ...
    geom_dir_z: geom_dir_z_cls = ...
    geom_levels: geom_levels_cls = ...
    geom_bgthread: geom_bgthread_cls = ...
    angular: angular_cls = ...
    p_jump: p_jump_cls = ...
    return_type = ...
