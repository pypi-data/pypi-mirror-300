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

from .method_13 import method as method_cls
from .auto_detection import auto_detection as auto_detection_cls
from .iterations_2 import iterations as iterations_cls
from .dissipation import dissipation as dissipation_cls

class first_scheme(Group):
    fluent_name = ...
    child_names = ...
    method: method_cls = ...
    auto_detection: auto_detection_cls = ...
    iterations: iterations_cls = ...
    dissipation: dissipation_cls = ...
