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

from .execute_settings_optimization import execute_settings_optimization as execute_settings_optimization_cls
from .execute_advanced_stabilization import execute_advanced_stabilization as execute_advanced_stabilization_cls
from .additional_stabilization_controls import additional_stabilization_controls as additional_stabilization_controls_cls
from .execute_additional_stability_controls import execute_additional_stability_controls as execute_additional_stability_controls_cls
from .velocity_limiting_treatment import velocity_limiting_treatment as velocity_limiting_treatment_cls

class solution_stabilization(Group):
    fluent_name = ...
    child_names = ...
    execute_settings_optimization: execute_settings_optimization_cls = ...
    execute_advanced_stabilization: execute_advanced_stabilization_cls = ...
    additional_stabilization_controls: additional_stabilization_controls_cls = ...
    execute_additional_stability_controls: execute_additional_stability_controls_cls = ...
    velocity_limiting_treatment: velocity_limiting_treatment_cls = ...
    return_type = ...
