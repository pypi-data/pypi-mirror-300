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

from .controls import controls as controls_cls
from .methods_1 import methods as methods_cls
from .report_definitions import report_definitions as report_definitions_cls
from .monitor import monitor as monitor_cls
from .cell_registers import cell_registers as cell_registers_cls
from .initialization import initialization as initialization_cls
from .calculation_activity import calculation_activity as calculation_activity_cls
from .run_calculation import run_calculation as run_calculation_cls

class solution(Group):
    fluent_name = ...
    child_names = ...
    controls: controls_cls = ...
    methods: methods_cls = ...
    report_definitions: report_definitions_cls = ...
    monitor: monitor_cls = ...
    cell_registers: cell_registers_cls = ...
    initialization: initialization_cls = ...
    calculation_activity: calculation_activity_cls = ...
    run_calculation: run_calculation_cls = ...
    return_type = ...
