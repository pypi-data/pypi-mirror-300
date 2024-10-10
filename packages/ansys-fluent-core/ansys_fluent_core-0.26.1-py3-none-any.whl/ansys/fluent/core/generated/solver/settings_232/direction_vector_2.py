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

from .x_component import x_component as x_component_cls
from .y_component import y_component as y_component_cls
from .z_component import z_component as z_component_cls

class direction_vector(Group):
    """
    'direction_vector' child.
    """

    fluent_name = "direction-vector"

    child_names = \
        ['x_component', 'y_component', 'z_component']

    _child_classes = dict(
        x_component=x_component_cls,
        y_component=y_component_cls,
        z_component=z_component_cls,
    )

    return_type = "<object object at 0x7fe5b8e2d710>"
