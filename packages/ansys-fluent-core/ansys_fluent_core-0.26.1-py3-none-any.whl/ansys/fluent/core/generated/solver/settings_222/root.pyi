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

from .file import file as file_cls
from .setup import setup as setup_cls
from .solution import solution as solution_cls
from .results import results as results_cls
from .parametric_studies import parametric_studies as parametric_studies_cls
from .current_parametric_study import current_parametric_study as current_parametric_study_cls

class root(Group):
    fluent_name = ...
    child_names = ...
    file: file_cls = ...
    setup: setup_cls = ...
    solution: solution_cls = ...
    results: results_cls = ...
    parametric_studies: parametric_studies_cls = ...
    current_parametric_study: current_parametric_study_cls = ...
    return_type = ...
