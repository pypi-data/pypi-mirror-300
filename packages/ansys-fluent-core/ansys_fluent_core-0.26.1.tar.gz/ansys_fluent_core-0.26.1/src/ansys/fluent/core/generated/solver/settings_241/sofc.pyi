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

from .enabled_13 import enabled as enabled_cls
from .electrochemistry import electrochemistry as electrochemistry_cls
from .model_parameters import model_parameters as model_parameters_cls
from .anode_interface import anode_interface as anode_interface_cls
from .cathode_interface import cathode_interface as cathode_interface_cls
from .tortuosity_interface import tortuosity_interface as tortuosity_interface_cls
from .pore_size_interface import pore_size_interface as pore_size_interface_cls
from .electric_field import electric_field as electric_field_cls
from .customized_udf import customized_udf as customized_udf_cls

class sofc(Group):
    fluent_name = ...
    child_names = ...
    enabled: enabled_cls = ...
    electrochemistry: electrochemistry_cls = ...
    model_parameters: model_parameters_cls = ...
    anode_interface: anode_interface_cls = ...
    cathode_interface: cathode_interface_cls = ...
    tortuosity_interface: tortuosity_interface_cls = ...
    pore_size_interface: pore_size_interface_cls = ...
    electric_field: electric_field_cls = ...
    customized_udf: customized_udf_cls = ...
    return_type = ...
