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

from .create_7 import create as create_cls
from .delete_1 import delete as delete_cls
from .rename import rename as rename_cls
from .list import list as list_cls
from .list_properties import list_properties as list_properties_cls
from .make_a_copy import make_a_copy as make_a_copy_cls
from .save_1 import save as save_cls
from .load import load as load_cls
from .get_list_of_valid_cell_function_names import get_list_of_valid_cell_function_names as get_list_of_valid_cell_function_names_cls
from .custom_field_functions_child import custom_field_functions_child


class custom_field_functions(NamedObject[custom_field_functions_child], CreatableNamedObjectMixin[custom_field_functions_child]):
    """
    Provides access to creating custom field function.
    """

    fluent_name = "custom-field-functions"

    command_names = \
        ['create', 'delete', 'rename', 'list', 'list_properties',
         'make_a_copy', 'save', 'load']

    query_names = \
        ['get_list_of_valid_cell_function_names']

    _child_classes = dict(
        create=create_cls,
        delete=delete_cls,
        rename=rename_cls,
        list=list_cls,
        list_properties=list_properties_cls,
        make_a_copy=make_a_copy_cls,
        save=save_cls,
        load=load_cls,
        get_list_of_valid_cell_function_names=get_list_of_valid_cell_function_names_cls,
    )

    child_object_type: custom_field_functions_child = custom_field_functions_child
    """
    child_object_type of custom_field_functions.
    """
