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

from typing import Union, List, Tuple

from .option_10 import option as option_cls
from .value import value as value_cls
from .rgp_table import rgp_table as rgp_table_cls

class molecular_weight(Group):
    fluent_name = ...
    child_names = ...
    option: option_cls = ...
    value: value_cls = ...
    rgp_table: rgp_table_cls = ...
    return_type = ...
