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

from .bodies import bodies as bodies_cls
from .groups import groups as groups_cls

class parts_child(Group):
    fluent_name = ...
    child_names = ...
    bodies: bodies_cls = ...
    groups: groups_cls = ...
    return_type = ...
