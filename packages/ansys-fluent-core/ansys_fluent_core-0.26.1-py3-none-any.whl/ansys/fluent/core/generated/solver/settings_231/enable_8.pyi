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

from .enable import enable as enable_cls
from .gradient_correction_mode import gradient_correction_mode as gradient_correction_mode_cls

class enable(Command):
    fluent_name = ...
    argument_names = ...
    enable: enable_cls = ...
    gradient_correction_mode: gradient_correction_mode_cls = ...
    return_type = ...
