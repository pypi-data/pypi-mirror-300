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

from .solution_based_initialization import solution_based_initialization as solution_based_initialization_cls
from .auto_adjust import auto_adjust as auto_adjust_cls
from .show_advancement_controls import show_advancement_controls as show_advancement_controls_cls
from .apply_precondition import apply_precondition as apply_precondition_cls
from .advancement import advancement as advancement_cls
from .under_relaxation_3 import under_relaxation as under_relaxation_cls
from .amg_1 import amg as amg_cls
from .stabilization_1 import stabilization as stabilization_cls
from .default_4 import default as default_cls

class controls(Group):
    fluent_name = ...
    child_names = ...
    solution_based_initialization: solution_based_initialization_cls = ...
    auto_adjust: auto_adjust_cls = ...
    show_advancement_controls: show_advancement_controls_cls = ...
    apply_precondition: apply_precondition_cls = ...
    advancement: advancement_cls = ...
    under_relaxation: under_relaxation_cls = ...
    amg: amg_cls = ...
    stabilization: stabilization_cls = ...
    command_names = ...

    def default(self, ):
        """
        Set controls to default.
        """

