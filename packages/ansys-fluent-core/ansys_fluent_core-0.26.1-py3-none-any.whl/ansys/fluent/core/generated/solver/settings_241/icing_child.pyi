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

from .name import name as name_cls
from .report_type import report_type as report_type_cls
from .create_output_parameter import create_output_parameter as create_output_parameter_cls

class icing_child(Group):
    fluent_name = ...
    child_names = ...
    name: name_cls = ...
    report_type: report_type_cls = ...
    command_names = ...

    def create_output_parameter(self, ):
        """
        'create_output_parameter' command.
        """

    return_type = ...
