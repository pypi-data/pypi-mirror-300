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

from .delete_1 import delete as delete_cls
from .rename import rename as rename_cls
from .list import list as list_cls
from .list_properties_1 import list_properties as list_properties_cls
from .make_a_copy import make_a_copy as make_a_copy_cls
from .display_2 import display as display_cls
from .copy_4 import copy as copy_cls
from .add_to_graphics import add_to_graphics as add_to_graphics_cls
from .clear_history import clear_history as clear_history_cls
from .xy_plot_child import xy_plot_child


class xy_plot(NamedObject[xy_plot_child], CreatableNamedObjectMixinOld[xy_plot_child]):
    """
    'xy_plot' child.
    """

    fluent_name = "xy-plot"

    command_names = \
        ['delete', 'rename', 'list', 'list_properties', 'make_a_copy',
         'display', 'copy', 'add_to_graphics', 'clear_history']

    _child_classes = dict(
        delete=delete_cls,
        rename=rename_cls,
        list=list_cls,
        list_properties=list_properties_cls,
        make_a_copy=make_a_copy_cls,
        display=display_cls,
        copy=copy_cls,
        add_to_graphics=add_to_graphics_cls,
        clear_history=clear_history_cls,
    )

    child_object_type: xy_plot_child = xy_plot_child
    """
    child_object_type of xy_plot.
    """
