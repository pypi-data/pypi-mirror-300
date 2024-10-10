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

from .list_properties import list_properties as list_properties_cls
from .shallow_wave_inputs_child import shallow_wave_inputs_child


class shallow_wave_inputs(ListObject[shallow_wave_inputs_child]):
    """
    Shallow Wave Inputs.
    """

    fluent_name = "shallow-wave-inputs"

    command_names = \
        ['list_properties']

    _child_classes = dict(
        list_properties=list_properties_cls,
    )

    child_object_type: shallow_wave_inputs_child = shallow_wave_inputs_child
    """
    child_object_type of shallow_wave_inputs.
    """
    return_type = "<object object at 0x7fd93fe3c8f0>"
