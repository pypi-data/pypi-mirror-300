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

from .settings_2 import settings as settings_cls
from .reset import reset as reset_cls
from .invert import invert as invert_cls

class transparency_options(Group):
    fluent_name = ...
    child_names = ...
    settings: settings_cls = ...
    reset: reset_cls = ...
    invert: invert_cls = ...
