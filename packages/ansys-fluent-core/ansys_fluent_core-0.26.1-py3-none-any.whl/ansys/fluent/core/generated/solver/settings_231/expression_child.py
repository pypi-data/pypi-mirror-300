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

from .list_valid_report_names import list_valid_report_names as list_valid_report_names_cls
from .define import define as define_cls
from .expr_value import expr_value as expr_value_cls
from .average_over import average_over as average_over_cls
from .old_props import old_props as old_props_cls

class expression_child(Group):
    """
    'child_object_type' of expression.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['list_valid_report_names', 'define', 'expr_value', 'average_over',
         'old_props']

    _child_classes = dict(
        list_valid_report_names=list_valid_report_names_cls,
        define=define_cls,
        expr_value=expr_value_cls,
        average_over=average_over_cls,
        old_props=old_props_cls,
    )

    return_type = "<object object at 0x7ff9d0a61160>"
