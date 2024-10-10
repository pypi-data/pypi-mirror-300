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

from .entropic_heat_enabled import entropic_heat_enabled as entropic_heat_enabled_cls
from .data_type_1 import data_type as data_type_cls
from .two_tables import two_tables as two_tables_cls
from .table_discharge import table_discharge as table_discharge_cls
from .table_charge import table_charge as table_charge_cls
from .udf_name import udf_name as udf_name_cls

class entropic_heat(Group):
    fluent_name = ...
    child_names = ...
    entropic_heat_enabled: entropic_heat_enabled_cls = ...
    data_type: data_type_cls = ...
    two_tables: two_tables_cls = ...
    table_discharge: table_discharge_cls = ...
    table_charge: table_charge_cls = ...
    udf_name: udf_name_cls = ...
    return_type = ...
