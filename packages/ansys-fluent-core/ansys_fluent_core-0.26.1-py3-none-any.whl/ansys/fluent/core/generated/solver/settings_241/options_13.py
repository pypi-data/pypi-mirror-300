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

from .option import option as option_cls
from .inside_1 import inside as inside_cls
from .outside import outside as outside_cls

class options(Group):
    """
    'options' child.
    """

    fluent_name = "options"

    child_names = \
        ['option', 'inside', 'outside']

    _child_classes = dict(
        option=option_cls,
        inside=inside_cls,
        outside=outside_cls,
    )

    return_type = "<object object at 0x7fd93f8cc580>"
