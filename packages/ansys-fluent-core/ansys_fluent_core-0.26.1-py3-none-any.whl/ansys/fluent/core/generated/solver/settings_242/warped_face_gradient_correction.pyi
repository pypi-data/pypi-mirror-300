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

from .enable_19 import enable as enable_cls
from .mode_1 import mode as mode_cls
from .turbulence_options import turbulence_options as turbulence_options_cls

class warped_face_gradient_correction(Group):
    fluent_name = ...
    child_names = ...
    enable: enable_cls = ...
    mode: mode_cls = ...
    turbulence_options: turbulence_options_cls = ...
