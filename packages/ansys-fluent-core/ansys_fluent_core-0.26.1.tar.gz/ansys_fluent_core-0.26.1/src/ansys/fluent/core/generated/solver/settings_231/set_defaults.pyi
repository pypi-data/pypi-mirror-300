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

from .set_defaults_child import set_defaults_child


class set_defaults(NamedObject[set_defaults_child], _NonCreatableNamedObjectMixin[set_defaults_child]):
    fluent_name = ...
    child_object_type: set_defaults_child = ...
    return_type = ...
