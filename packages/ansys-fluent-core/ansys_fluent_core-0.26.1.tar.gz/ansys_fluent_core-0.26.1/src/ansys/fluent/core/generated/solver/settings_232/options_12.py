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
from .constant_1 import constant as constant_cls
from .variable_1 import variable as variable_cls

class options(Group):
    """
    'options' child.
    """

    fluent_name = "options"

    child_names = \
        ['option', 'constant', 'variable']

    _child_classes = dict(
        option=option_cls,
        constant=constant_cls,
        variable=variable_cls,
    )

    return_type = "<object object at 0x7fe5b8f471c0>"
