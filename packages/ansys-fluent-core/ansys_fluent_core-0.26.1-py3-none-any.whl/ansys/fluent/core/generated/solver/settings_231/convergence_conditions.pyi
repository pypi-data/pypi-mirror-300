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

from .convergence_reports import convergence_reports as convergence_reports_cls
from .frequency_1 import frequency as frequency_cls
from .condition import condition as condition_cls
from .check_for import check_for as check_for_cls

class convergence_conditions(Group):
    fluent_name = ...
    child_names = ...
    convergence_reports: convergence_reports_cls = ...
    frequency: frequency_cls = ...
    condition: condition_cls = ...
    check_for: check_for_cls = ...
    return_type = ...
