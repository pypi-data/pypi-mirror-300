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
from .custom_field_function import custom_field_function as custom_field_function_cls

class create(CommandWithPositionalArgs):
    """
    Create a custom field function.
    
    Parameters
    ----------
        name : str
            Specify the name for the custom field function.
        custom_field_function : str
            Specify the custom field function.
    
    """

    fluent_name = "create"

    argument_names = \
        ['name', 'custom_field_function']

    _child_classes = dict(
        name=name_cls,
        custom_field_function=custom_field_function_cls,
    )

