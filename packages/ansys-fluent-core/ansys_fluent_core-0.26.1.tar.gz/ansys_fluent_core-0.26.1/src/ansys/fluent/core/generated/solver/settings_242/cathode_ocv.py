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

from .method_4 import method as method_cls
from .value_2 import value as value_cls
from .user_defined import user_defined as user_defined_cls

class cathode_ocv(Group):
    """
    Set equilibium potential at cathode.
    """

    fluent_name = "cathode-ocv"

    child_names = \
        ['method', 'value', 'user_defined']

    _child_classes = dict(
        method=method_cls,
        value=value_cls,
        user_defined=user_defined_cls,
    )

