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

from .selection_type import selection_type as selection_type_cls
from .settings_5 import settings as settings_cls
from .reset import reset as reset_cls

class clip_sphere_options(Group):
    fluent_name = ...
    child_names = ...
    selection_type: selection_type_cls = ...
    settings: settings_cls = ...
    reset: reset_cls = ...
