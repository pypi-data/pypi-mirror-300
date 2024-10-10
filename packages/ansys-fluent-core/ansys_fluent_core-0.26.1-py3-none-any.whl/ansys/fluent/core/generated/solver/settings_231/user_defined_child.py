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

from .retain_instantaneous_values import retain_instantaneous_values as retain_instantaneous_values_cls
from .input_params import input_params as input_params_cls
from .function_name import function_name as function_name_cls
from .average_over import average_over as average_over_cls
from .old_props import old_props as old_props_cls

class user_defined_child(Group):
    """
    'child_object_type' of user_defined.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['retain_instantaneous_values', 'input_params', 'function_name',
         'average_over', 'old_props']

    _child_classes = dict(
        retain_instantaneous_values=retain_instantaneous_values_cls,
        input_params=input_params_cls,
        function_name=function_name_cls,
        average_over=average_over_cls,
        old_props=old_props_cls,
    )

    return_type = "<object object at 0x7ff9d0a60fd0>"
