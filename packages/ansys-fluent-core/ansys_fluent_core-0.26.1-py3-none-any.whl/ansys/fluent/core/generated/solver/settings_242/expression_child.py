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

from .name import name as name_cls
from .average_over import average_over as average_over_cls
from .expr_value import expr_value as expr_value_cls
from .define import define as define_cls
from .list_valid_report_names import list_valid_report_names as list_valid_report_names_cls
from .output_parameter_1 import output_parameter as output_parameter_cls
from .create_output_parameter import create_output_parameter as create_output_parameter_cls

class expression_child(Group):
    """
    'child_object_type' of expression.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'average_over', 'expr_value', 'define',
         'list_valid_report_names', 'output_parameter']

    command_names = \
        ['create_output_parameter']

    _child_classes = dict(
        name=name_cls,
        average_over=average_over_cls,
        expr_value=expr_value_cls,
        define=define_cls,
        list_valid_report_names=list_valid_report_names_cls,
        output_parameter=output_parameter_cls,
        create_output_parameter=create_output_parameter_cls,
    )

