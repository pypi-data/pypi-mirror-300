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

from .fan_child import fan_child


class fan(NamedObject[fan_child], _NonCreatableNamedObjectMixin[fan_child]):
    fluent_name = ...
    child_object_type: fan_child = ...
    return_type = ...
