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
from .report_plots_child import report_plots_child


class report_plots(NamedObject[report_plots_child], CreatableNamedObjectMixinOld[report_plots_child]):
    """
    Available options related to report plots.
    """

    fluent_name = "report-plots"

    command_names = \
        ['delete', 'rename', 'list', 'list_properties', 'make_a_copy']

    _child_classes = dict(
        delete=delete_cls,
        rename=rename_cls,
        list=list_cls,
        list_properties=list_properties_cls,
        make_a_copy=make_a_copy_cls,
    )

    child_object_type: report_plots_child = report_plots_child
    """
    child_object_type of report_plots.
    """
