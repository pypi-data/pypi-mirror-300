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

from .polar_pair_list_child import polar_pair_list_child


class polar_pair_list(ListObject[polar_pair_list_child]):
    fluent_name = ...
    child_object_type: polar_pair_list_child = ...
    return_type = ...
