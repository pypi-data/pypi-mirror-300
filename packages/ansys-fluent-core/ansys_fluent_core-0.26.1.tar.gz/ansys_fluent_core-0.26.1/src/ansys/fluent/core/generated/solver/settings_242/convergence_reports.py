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
from .convergence_reports_child import convergence_reports_child


class convergence_reports(NamedObject[convergence_reports_child], CreatableNamedObjectMixinOld[convergence_reports_child]):
    """
    Available options related to creating convergence reports.
    """

    fluent_name = "convergence-reports"

    command_names = \
        ['delete', 'rename', 'list', 'list_properties', 'make_a_copy']

    _child_classes = dict(
        delete=delete_cls,
        rename=rename_cls,
        list=list_cls,
        list_properties=list_properties_cls,
        make_a_copy=make_a_copy_cls,
    )

    child_object_type: convergence_reports_child = convergence_reports_child
    """
    child_object_type of convergence_reports.
    """
