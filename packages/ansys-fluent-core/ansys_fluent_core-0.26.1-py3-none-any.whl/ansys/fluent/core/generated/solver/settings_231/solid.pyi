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

from .solid_child import solid_child


class solid(NamedObject[solid_child], CreatableNamedObjectMixinOld[solid_child]):
    fluent_name = ...
    child_object_type: solid_child = ...
    return_type = ...
