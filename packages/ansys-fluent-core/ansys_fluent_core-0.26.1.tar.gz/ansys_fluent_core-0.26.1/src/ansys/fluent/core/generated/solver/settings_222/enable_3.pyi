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

from .enable_fast_mode import enable_fast_mode as enable_fast_mode_cls
from .enable_memory_saving_mode import enable_memory_saving_mode as enable_memory_saving_mode_cls
from .disable_warped_face_gradient_correction import disable_warped_face_gradient_correction as disable_warped_face_gradient_correction_cls

class enable(Group):
    fluent_name = ...
    child_names = ...
    enable_fast_mode: enable_fast_mode_cls = ...
    enable_memory_saving_mode: enable_memory_saving_mode_cls = ...
    command_names = ...

    def disable_warped_face_gradient_correction(self, ):
        """
        'disable_warped_face_gradient_correction' command.
        """

    return_type = ...
