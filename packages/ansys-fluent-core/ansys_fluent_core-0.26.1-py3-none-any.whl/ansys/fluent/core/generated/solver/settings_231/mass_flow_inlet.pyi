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

from .mass_flow_inlet_child import mass_flow_inlet_child


class mass_flow_inlet(NamedObject[mass_flow_inlet_child], _NonCreatableNamedObjectMixin[mass_flow_inlet_child]):
    fluent_name = ...
    child_object_type: mass_flow_inlet_child = ...
    return_type = ...
