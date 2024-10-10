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
from .value_1 import value as value_cls
from .profile_name import profile_name as profile_name_cls
from .field_name import field_name as field_name_cls
from .udf import udf as udf_cls

class ksgs(Group):
    """
    'ksgs' child.
    """

    fluent_name = "ksgs"

    child_names = \
        ['option', 'value', 'profile_name', 'field_name', 'udf']

    _child_classes = dict(
        option=option_cls,
        value=value_cls,
        profile_name=profile_name_cls,
        field_name=field_name_cls,
        udf=udf_cls,
    )

    return_type = "<object object at 0x7fe5ba361d50>"
