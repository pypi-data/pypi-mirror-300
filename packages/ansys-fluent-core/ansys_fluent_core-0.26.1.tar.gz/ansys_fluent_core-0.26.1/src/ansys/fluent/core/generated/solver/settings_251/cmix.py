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

from .option_6 import option as option_cls
from .value_3 import value as value_cls
from .expression_2 import expression as expression_cls
from .user_defined_3 import user_defined as user_defined_cls

class cmix(Group):
    """
    Set the GEKO model coefficient CMIX.
    """

    fluent_name = "cmix"

    child_names = \
        ['option', 'value', 'expression', 'user_defined']

    _child_classes = dict(
        option=option_cls,
        value=value_cls,
        expression=expression_cls,
        user_defined=user_defined_cls,
    )

