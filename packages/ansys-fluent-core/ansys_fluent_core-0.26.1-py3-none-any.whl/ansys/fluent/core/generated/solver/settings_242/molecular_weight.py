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

from .option_12 import option as option_cls
from .value_11 import value as value_cls
from .rgp_table import rgp_table as rgp_table_cls

class molecular_weight(Group):
    """
    Molecular-weight property setting for this material.
    """

    fluent_name = "molecular-weight"

    child_names = \
        ['option', 'value', 'rgp_table']

    _child_classes = dict(
        option=option_cls,
        value=value_cls,
        rgp_table=rgp_table_cls,
    )

