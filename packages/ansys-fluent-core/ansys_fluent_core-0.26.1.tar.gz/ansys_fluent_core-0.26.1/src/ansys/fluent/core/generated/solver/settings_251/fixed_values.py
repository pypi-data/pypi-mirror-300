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

from .enable_15 import enable as enable_cls
from .cylindrical_fixed_var import cylindrical_fixed_var as cylindrical_fixed_var_cls
from .variables import variables as variables_cls

class fixed_values(Group):
    """
    Allows to change fixed-values model variables or settings.
    """

    fluent_name = "fixed-values"

    child_names = \
        ['enable', 'cylindrical_fixed_var', 'variables']

    _child_classes = dict(
        enable=enable_cls,
        cylindrical_fixed_var=cylindrical_fixed_var_cls,
        variables=variables_cls,
    )

    _child_aliases = dict(
        fixed="enable",
        fixes="variables",
    )

