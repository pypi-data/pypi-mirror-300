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

from .number_of_blades import number_of_blades as number_of_blades_cls
from .rotor_speed import rotor_speed as rotor_speed_cls
from .tip_radius import tip_radius as tip_radius_cls
from .root_radius import root_radius as root_radius_cls

class basic_info(Group):
    fluent_name = ...
    child_names = ...
    number_of_blades: number_of_blades_cls = ...
    rotor_speed: rotor_speed_cls = ...
    tip_radius: tip_radius_cls = ...
    root_radius: root_radius_cls = ...
