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

from .option_3 import option as option_cls
from .automatic import automatic as automatic_cls
from .manual import manual as manual_cls

class coloring(Group):
    fluent_name = ...
    child_names = ...
    option: option_cls = ...
    automatic: automatic_cls = ...
    manual: manual_cls = ...
    return_type = ...
