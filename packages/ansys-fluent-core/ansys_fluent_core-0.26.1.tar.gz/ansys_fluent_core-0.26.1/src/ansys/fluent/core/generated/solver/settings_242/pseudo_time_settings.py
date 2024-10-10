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

from .verbosity_13 import verbosity as verbosity_cls
from .time_step_method_1 import time_step_method as time_step_method_cls

class pseudo_time_settings(Group):
    """
    Enter the pseudo time method menu.
    """

    fluent_name = "pseudo-time-settings"

    child_names = \
        ['verbosity', 'time_step_method']

    _child_classes = dict(
        verbosity=verbosity_cls,
        time_step_method=time_step_method_cls,
    )

