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

from .named_expressions_child import named_expressions_child


class named_expressions(NamedObject[named_expressions_child], CreatableNamedObjectMixinOld[named_expressions_child]):
    fluent_name = ...
    child_object_type: named_expressions_child = ...
    return_type = ...
