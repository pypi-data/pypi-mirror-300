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

from .axis_direction_component_child import axis_direction_component_child


class component_of_wall_translation(ListObject[axis_direction_component_child]):
    fluent_name = ...
    child_object_type: axis_direction_component_child = ...
    return_type = ...
