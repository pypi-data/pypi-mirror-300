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

from .item import item as item_cls
from .value_1 import value as value_cls

class data_points_child(Group):
    """
    'child_object_type' of data_points.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['item', 'value']

    _child_classes = dict(
        item=item_cls,
        value=value_cls,
    )

