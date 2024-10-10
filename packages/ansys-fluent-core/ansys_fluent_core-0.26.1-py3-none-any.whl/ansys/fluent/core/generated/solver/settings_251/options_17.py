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

from .option_45 import option as option_cls
from .constant_3 import constant as constant_cls
from .variable_1 import variable as variable_cls

class options(Group):
    """
    Choose the options Constant or Variable.
    """

    fluent_name = "options"

    child_names = \
        ['option', 'constant', 'variable']

    _child_classes = dict(
        option=option_cls,
        constant=constant_cls,
        variable=variable_cls,
    )

