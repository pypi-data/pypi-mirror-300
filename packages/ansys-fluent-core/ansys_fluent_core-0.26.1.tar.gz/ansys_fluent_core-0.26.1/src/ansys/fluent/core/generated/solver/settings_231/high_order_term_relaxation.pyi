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

from .enable_5 import enable as enable_cls
from .options_3 import options as options_cls

class high_order_term_relaxation(Group):
    fluent_name = ...
    child_names = ...
    enable: enable_cls = ...
    options: options_cls = ...
    return_type = ...
