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

from .periodic_child import periodic_child


class periodic(NamedObject[periodic_child], _NonCreatableNamedObjectMixin[periodic_child]):
    fluent_name = ...
    child_object_type: periodic_child = ...
    return_type = ...
