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

from .rk2 import rk2 as rk2_cls

class fast_transient_settings(Group):
    """
    'fast_transient_settings' child.
    """

    fluent_name = "fast-transient-settings"

    child_names = \
        ['rk2']

    _child_classes = dict(
        rk2=rk2_cls,
    )

    return_type = "<object object at 0x7f82c58609f0>"
