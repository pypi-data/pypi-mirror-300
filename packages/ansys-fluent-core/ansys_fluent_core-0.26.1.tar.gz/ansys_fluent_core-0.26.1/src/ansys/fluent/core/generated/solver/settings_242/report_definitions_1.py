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
from .print_to_console import print_to_console as print_to_console_cls
from .write_to_file_6 import write_to_file as write_to_file_cls
from .report_definitions_child import report_definitions_child


class report_definitions(NamedObject[report_definitions_child], CreatableNamedObjectMixinOld[report_definitions_child]):
    """
    'report_definitions' child.
    """

    fluent_name = "report-definitions"

    command_names = \
        ['delete', 'rename', 'list', 'list_properties', 'make_a_copy',
         'print_to_console', 'write_to_file']

    _child_classes = dict(
        delete=delete_cls,
        rename=rename_cls,
        list=list_cls,
        list_properties=list_properties_cls,
        make_a_copy=make_a_copy_cls,
        print_to_console=print_to_console_cls,
        write_to_file=write_to_file_cls,
    )

    child_object_type: report_definitions_child = report_definitions_child
    """
    child_object_type of report_definitions.
    """
