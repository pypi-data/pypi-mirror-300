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

from .distance_option import distance_option as distance_option_cls
from .boundary_list import boundary_list as boundary_list_cls

class boundary(Group):
    """
    'boundary' child.
    """

    fluent_name = "boundary"

    child_names = \
        ['distance_option', 'boundary_list']

    _child_classes = dict(
        distance_option=distance_option_cls,
        boundary_list=boundary_list_cls,
    )

