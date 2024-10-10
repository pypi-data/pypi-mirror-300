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

from .name_6 import name as name_cls
from .option_1 import option as option_cls
from .zones_2 import zones as zones_cls
from .split_direction import split_direction as split_direction_cls
from .number_of_divisions import number_of_divisions as number_of_divisions_cls
from .force_direction import force_direction as force_direction_cls
from .moment_center import moment_center as moment_center_cls
from .moment_axis import moment_axis as moment_axis_cls
from .x_axis_quantity import x_axis_quantity as x_axis_quantity_cls
from .compute_from_stats import compute_from_stats as compute_from_stats_cls
from .axes import axes as axes_cls
from .curves import curves as curves_cls
from .plot_7 import plot as plot_cls

class cumulative_plot_child(Group):
    """
    'child_object_type' of cumulative_plot.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'option', 'zones', 'split_direction', 'number_of_divisions',
         'force_direction', 'moment_center', 'moment_axis', 'x_axis_quantity',
         'compute_from_stats', 'axes', 'curves']

    command_names = \
        ['plot']

    _child_classes = dict(
        name=name_cls,
        option=option_cls,
        zones=zones_cls,
        split_direction=split_direction_cls,
        number_of_divisions=number_of_divisions_cls,
        force_direction=force_direction_cls,
        moment_center=moment_center_cls,
        moment_axis=moment_axis_cls,
        x_axis_quantity=x_axis_quantity_cls,
        compute_from_stats=compute_from_stats_cls,
        axes=axes_cls,
        curves=curves_cls,
        plot=plot_cls,
    )

