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

from .file_name_1_3 import file_name_1 as file_name_1_cls

class read_simulation_report_template_file(Command):
    fluent_name = ...
    argument_names = ...
    file_name: file_name_1_cls = ...
