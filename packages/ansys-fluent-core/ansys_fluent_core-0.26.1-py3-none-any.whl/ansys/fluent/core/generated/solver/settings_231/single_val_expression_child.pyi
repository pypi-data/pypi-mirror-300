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

from .retain_instantaneous_values import retain_instantaneous_values as retain_instantaneous_values_cls
from .list_valid_report_names import list_valid_report_names as list_valid_report_names_cls
from .define import define as define_cls
from .average_over import average_over as average_over_cls
from .old_props import old_props as old_props_cls

class single_val_expression_child(Group):
    fluent_name = ...
    child_names = ...
    retain_instantaneous_values: retain_instantaneous_values_cls = ...
    list_valid_report_names: list_valid_report_names_cls = ...
    define: define_cls = ...
    average_over: average_over_cls = ...
    old_props: old_props_cls = ...
    return_type = ...
