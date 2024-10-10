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
from .print_to_console import print_to_console as print_to_console_cls
from .write_to_file_7 import write_to_file as write_to_file_cls
from .named_expressions_child_1 import named_expressions_child


class named_expressions(NamedObject[named_expressions_child], CreatableNamedObjectMixin[named_expressions_child]):
    """
    Enter Named Expression parameters menu.
    """

    fluent_name = "named-expressions"

    command_names = \
        ['create', 'delete', 'rename', 'list', 'list_properties',
         'make_a_copy', 'print_to_console', 'write_to_file']

    _child_classes = dict(
        create=create_cls,
        delete=delete_cls,
        rename=rename_cls,
        list=list_cls,
        list_properties=list_properties_cls,
        make_a_copy=make_a_copy_cls,
        print_to_console=print_to_console_cls,
        write_to_file=write_to_file_cls,
    )

    child_object_type: named_expressions_child = named_expressions_child
    """
    child_object_type of named_expressions.
    """
