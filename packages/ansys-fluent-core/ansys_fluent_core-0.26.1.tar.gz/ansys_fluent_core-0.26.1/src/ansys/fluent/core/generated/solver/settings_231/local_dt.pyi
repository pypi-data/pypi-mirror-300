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

from .local_dt_child import local_dt_child


class local_dt(NamedObject[local_dt_child], _NonCreatableNamedObjectMixin[local_dt_child]):
    fluent_name = ...
    child_object_type: local_dt_child = ...
    return_type = ...
