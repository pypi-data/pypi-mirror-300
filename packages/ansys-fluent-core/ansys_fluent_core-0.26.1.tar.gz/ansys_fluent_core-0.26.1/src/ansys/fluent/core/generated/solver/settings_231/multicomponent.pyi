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

from .multicomponent_child import multicomponent_child


class multicomponent(NamedObject[multicomponent_child], _NonCreatableNamedObjectMixin[multicomponent_child]):
    fluent_name = ...
    child_object_type: multicomponent_child = ...
    return_type = ...
