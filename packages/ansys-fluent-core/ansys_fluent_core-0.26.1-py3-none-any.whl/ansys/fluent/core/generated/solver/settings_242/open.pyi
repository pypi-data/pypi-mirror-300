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

from .project_filename_1 import project_filename_1 as project_filename_1_cls
from .load_case import load_case as load_case_cls

class open(Command):
    fluent_name = ...
    argument_names = ...
    project_filename: project_filename_1_cls = ...
    load_case: load_case_cls = ...
