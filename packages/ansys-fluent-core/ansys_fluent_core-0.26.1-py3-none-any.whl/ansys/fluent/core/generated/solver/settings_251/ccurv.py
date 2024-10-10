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

from .option_8 import option as option_cls
from .value_4 import value as value_cls
from .expression_4 import expression as expression_cls
from .user_defined_7 import user_defined as user_defined_cls

class ccurv(Group):
    """
    Set the curvature correction coefficient CCURV.
    """

    fluent_name = "ccurv"

    child_names = \
        ['option', 'value', 'expression', 'user_defined']

    _child_classes = dict(
        option=option_cls,
        value=value_cls,
        expression=expression_cls,
        user_defined=user_defined_cls,
    )

