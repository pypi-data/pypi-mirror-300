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

from .name_19 import name as name_cls
from .custom_field_function_1 import custom_field_function as custom_field_function_cls

class custom_field_functions_child(Group):
    """
    'child_object_type' of custom_field_functions.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'custom_field_function']

    _child_classes = dict(
        name=name_cls,
        custom_field_function=custom_field_function_cls,
    )

