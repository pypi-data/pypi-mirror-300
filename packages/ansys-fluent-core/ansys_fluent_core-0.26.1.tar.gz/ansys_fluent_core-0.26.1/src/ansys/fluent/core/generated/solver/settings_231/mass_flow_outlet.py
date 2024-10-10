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

from .mass_flow_inlet_child import mass_flow_inlet_child


class mass_flow_outlet(NamedObject[mass_flow_inlet_child], _NonCreatableNamedObjectMixin[mass_flow_inlet_child]):
    """
    'mass_flow_outlet' child.
    """

    fluent_name = "mass-flow-outlet"

    child_object_type: mass_flow_inlet_child = mass_flow_inlet_child
    """
    child_object_type of mass_flow_outlet.
    """
    return_type = "<object object at 0x7ff9d1cf3e10>"
