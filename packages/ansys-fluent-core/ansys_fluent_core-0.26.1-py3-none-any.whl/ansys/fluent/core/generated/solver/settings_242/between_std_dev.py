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

from .lower import lower as lower_cls
from .upper import upper as upper_cls

class between_std_dev(Group):
    """
    'between_std_dev' child.
    """

    fluent_name = "between-std-dev"

    child_names = \
        ['lower', 'upper']

    _child_classes = dict(
        lower=lower_cls,
        upper=upper_cls,
    )

