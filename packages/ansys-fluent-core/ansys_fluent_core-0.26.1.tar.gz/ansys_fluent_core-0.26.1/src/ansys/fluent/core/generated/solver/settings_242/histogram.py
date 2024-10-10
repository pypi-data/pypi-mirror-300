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

from .cell_function_1 import cell_function as cell_function_cls
from .auto_range_2 import auto_range as auto_range_cls
from .minimum_3 import minimum as minimum_cls
from .maximum_3 import maximum as maximum_cls
from .num_divisions import num_divisions as num_divisions_cls
from .zones_7 import zones as zones_cls
from .axes import axes as axes_cls
from .curves import curves as curves_cls
from .print_4 import print as print_cls
from .plot_5 import plot as plot_cls
from .write_3 import write as write_cls
from .get_values import get_values as get_values_cls

class histogram(Group):
    """
    Provides access to create new and edit existing histogram plots.
    """

    fluent_name = "histogram"

    child_names = \
        ['cell_function', 'auto_range', 'minimum', 'maximum', 'num_divisions',
         'zones', 'axes', 'curves']

    command_names = \
        ['print', 'plot', 'write']

    query_names = \
        ['get_values']

    _child_classes = dict(
        cell_function=cell_function_cls,
        auto_range=auto_range_cls,
        minimum=minimum_cls,
        maximum=maximum_cls,
        num_divisions=num_divisions_cls,
        zones=zones_cls,
        axes=axes_cls,
        curves=curves_cls,
        print=print_cls,
        plot=plot_cls,
        write=write_cls,
        get_values=get_values_cls,
    )

