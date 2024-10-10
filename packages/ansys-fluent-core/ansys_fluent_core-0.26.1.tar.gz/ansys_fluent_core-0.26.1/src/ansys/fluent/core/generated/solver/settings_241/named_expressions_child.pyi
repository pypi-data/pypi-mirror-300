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

from .name_1 import name as name_cls
from .definition import definition as definition_cls
from .description import description as description_cls
from .parameterid import parameterid as parameterid_cls
from .parametername import parametername as parametername_cls
from .unit_2 import unit as unit_cls
from .input_parameter import input_parameter as input_parameter_cls
from .output_parameter import output_parameter as output_parameter_cls
from .get_value import get_value as get_value_cls

class named_expressions_child(Group):
    fluent_name = ...
    child_names = ...
    name: name_cls = ...
    definition: definition_cls = ...
    description: description_cls = ...
    parameterid: parameterid_cls = ...
    parametername: parametername_cls = ...
    unit: unit_cls = ...
    input_parameter: input_parameter_cls = ...
    output_parameter: output_parameter_cls = ...
    query_names = ...

    def get_value(self, ):
        """
        'get_value' query.
        """

    return_type = ...
