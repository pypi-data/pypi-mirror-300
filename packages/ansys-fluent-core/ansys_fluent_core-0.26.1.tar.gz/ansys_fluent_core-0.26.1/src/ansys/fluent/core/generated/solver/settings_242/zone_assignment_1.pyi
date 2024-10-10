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

from .active_zone import active_zone as active_zone_cls
from .passive_zone import passive_zone as passive_zone_cls
from .passive_zone_tab import passive_zone_tab as passive_zone_tab_cls
from .virtual_connection import virtual_connection as virtual_connection_cls
from .virtual_connection_file import virtual_connection_file as virtual_connection_file_cls
from .positive_tab import positive_tab as positive_tab_cls
from .negative_tab import negative_tab as negative_tab_cls
from .print_battery_connection import print_battery_connection as print_battery_connection_cls

class zone_assignment(Group):
    fluent_name = ...
    child_names = ...
    active_zone: active_zone_cls = ...
    passive_zone: passive_zone_cls = ...
    passive_zone_tab: passive_zone_tab_cls = ...
    virtual_connection: virtual_connection_cls = ...
    virtual_connection_file: virtual_connection_file_cls = ...
    positive_tab: positive_tab_cls = ...
    negative_tab: negative_tab_cls = ...
    command_names = ...

    def print_battery_connection(self, ):
        """
        Print battery connection information.
        """

