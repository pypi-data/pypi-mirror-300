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

from .correction_tolerance_child import correction_tolerance_child


class correction_tolerance(NamedObject[correction_tolerance_child], CreatableNamedObjectMixinOld[correction_tolerance_child]):
    fluent_name = ...
    child_object_type: correction_tolerance_child = ...
    return_type = ...
