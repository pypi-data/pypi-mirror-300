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

from .type_2 import type as type_cls
from .formula import formula as formula_cls
from .new_name_1 import new_name as new_name_cls
from .new_formula import new_formula as new_formula_cls

class copy_by_formula(Command):
    fluent_name = ...
    argument_names = ...
    type: type_cls = ...
    formula: formula_cls = ...
    new_name: new_name_cls = ...
    new_formula: new_formula_cls = ...
