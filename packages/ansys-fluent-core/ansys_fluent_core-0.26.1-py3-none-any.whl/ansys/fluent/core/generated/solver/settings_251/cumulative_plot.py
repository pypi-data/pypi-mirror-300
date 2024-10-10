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

from .create_1 import create as create_cls
from .delete_1 import delete as delete_cls
from .rename import rename as rename_cls
from .list import list as list_cls
from .list_properties import list_properties as list_properties_cls
from .make_a_copy import make_a_copy as make_a_copy_cls
from .plot_6 import plot as plot_cls
from .write_5 import write as write_cls
from .cumulative_plot_child import cumulative_plot_child


class cumulative_plot(NamedObject[cumulative_plot_child], CreatableNamedObjectMixin[cumulative_plot_child]):
    """
    Cumulative plots.
    """

    fluent_name = "cumulative-plot"

    command_names = \
        ['create', 'delete', 'rename', 'list', 'list_properties',
         'make_a_copy', 'plot', 'write']

    _child_classes = dict(
        create=create_cls,
        delete=delete_cls,
        rename=rename_cls,
        list=list_cls,
        list_properties=list_properties_cls,
        make_a_copy=make_a_copy_cls,
        plot=plot_cls,
        write=write_cls,
    )

    child_object_type: cumulative_plot_child = cumulative_plot_child
    """
    child_object_type of cumulative_plot.
    """
