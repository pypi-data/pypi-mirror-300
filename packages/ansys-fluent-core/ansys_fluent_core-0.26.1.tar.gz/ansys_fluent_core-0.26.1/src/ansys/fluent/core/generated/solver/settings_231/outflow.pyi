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

from .outflow_child import outflow_child


class outflow(NamedObject[outflow_child], _NonCreatableNamedObjectMixin[outflow_child]):
    fluent_name = ...
    child_object_type: outflow_child = ...
    return_type = ...
