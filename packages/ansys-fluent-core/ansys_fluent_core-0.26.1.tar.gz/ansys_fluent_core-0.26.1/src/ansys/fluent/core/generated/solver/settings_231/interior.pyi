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

from .interior_child import interior_child


class interior(NamedObject[interior_child], _NonCreatableNamedObjectMixin[interior_child]):
    fluent_name = ...
    child_object_type: interior_child = ...
    return_type = ...
