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

from .interface_child import interface_child


class interface(NamedObject[interface_child], _NonCreatableNamedObjectMixin[interface_child]):
    fluent_name = ...
    child_object_type: interface_child = ...
    return_type = ...
