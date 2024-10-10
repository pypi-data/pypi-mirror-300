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

from .enable_13 import enable as enable_cls

class electrode(Group):
    """
    Zone is electrode.
    """

    fluent_name = "electrode"

    child_names = \
        ['enable']

    _child_classes = dict(
        enable=enable_cls,
    )

    _child_aliases = dict(
        electrode="enable",
    )

