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

from .id_2 import id as id_cls
from .condition_1 import condition as condition_cls
from .observable_3 import observable as observable_cls
from .goal import goal as goal_cls
from .value_24 import value as value_cls
from .value_as_percentage import value_as_percentage as value_as_percentage_cls
from .lower_bound import lower_bound as lower_bound_cls
from .upper_bound import upper_bound as upper_bound_cls
from .tolerance_8 import tolerance as tolerance_cls
from .tolerance_as_percentage import tolerance_as_percentage as tolerance_as_percentage_cls

class objectives_child(Group):
    """
    'child_object_type' of objectives.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['id', 'condition', 'observable', 'goal', 'value',
         'value_as_percentage', 'lower_bound', 'upper_bound', 'tolerance',
         'tolerance_as_percentage']

    _child_classes = dict(
        id=id_cls,
        condition=condition_cls,
        observable=observable_cls,
        goal=goal_cls,
        value=value_cls,
        value_as_percentage=value_as_percentage_cls,
        lower_bound=lower_bound_cls,
        upper_bound=upper_bound_cls,
        tolerance=tolerance_cls,
        tolerance_as_percentage=tolerance_as_percentage_cls,
    )

    _child_aliases = dict(
        step_size="value",
        value_as_percentage="as_percentage",
    )

