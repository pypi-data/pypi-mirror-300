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

from .polar_func_type import polar_func_type as polar_func_type_cls
from .polar_expression import polar_expression as polar_expression_cls
from .polar_data_pairs import polar_data_pairs as polar_data_pairs_cls
from .read_polar_dist_func_from_file import read_polar_dist_func_from_file as read_polar_dist_func_from_file_cls
from .write_polar_dist_func_to_file import write_polar_dist_func_to_file as write_polar_dist_func_to_file_cls

class polar_distribution_function_settings(Group):
    """
    Polar distribution function settings.
    """

    fluent_name = "polar-distribution-function-settings"

    child_names = \
        ['polar_func_type', 'polar_expression', 'polar_data_pairs']

    command_names = \
        ['read_polar_dist_func_from_file', 'write_polar_dist_func_to_file']

    _child_classes = dict(
        polar_func_type=polar_func_type_cls,
        polar_expression=polar_expression_cls,
        polar_data_pairs=polar_data_pairs_cls,
        read_polar_dist_func_from_file=read_polar_dist_func_from_file_cls,
        write_polar_dist_func_to_file=write_polar_dist_func_to_file_cls,
    )

    _child_aliases = dict(
        mc_polar_expr="polar_expression",
        polar_pair_list="polar_data_pairs",
    )

