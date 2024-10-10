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

from .oil_flow import oil_flow as oil_flow_cls
from .reverse import reverse as reverse_cls
from .node_values_1 import node_values as node_values_cls
from .relative_1 import relative as relative_cls

class options(Group):
    """
    'options' child.
    """

    fluent_name = "options"

    child_names = \
        ['oil_flow', 'reverse', 'node_values', 'relative']

    _child_classes = dict(
        oil_flow=oil_flow_cls,
        reverse=reverse_cls,
        node_values=node_values_cls,
        relative=relative_cls,
    )

    return_type = "<object object at 0x7f82c5863ce0>"
