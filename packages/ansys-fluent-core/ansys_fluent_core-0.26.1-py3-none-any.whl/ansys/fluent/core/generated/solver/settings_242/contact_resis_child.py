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

from .zone_name_7 import zone_name as zone_name_cls
from .value_4 import value as value_cls

class contact_resis_child(Group):
    """
    'child_object_type' of contact_resis.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['zone_name', 'value']

    _child_classes = dict(
        zone_name=zone_name_cls,
        value=value_cls,
    )

