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

from .wave_list_shallow_child import wave_list_shallow_child


class wave_list_shallow(ListObject[wave_list_shallow_child]):
    fluent_name = ...
    child_object_type: wave_list_shallow_child = ...
    return_type = ...
