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

from .equations_child import equations_child


class equations(NamedObject[equations_child], _NonCreatableNamedObjectMixin[equations_child]):
    fluent_name = ...
    child_object_type: equations_child = ...
    return_type = ...
