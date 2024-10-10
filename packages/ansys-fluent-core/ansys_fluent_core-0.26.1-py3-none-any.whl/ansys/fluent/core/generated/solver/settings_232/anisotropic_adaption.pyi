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

from typing import Union, List, Tuple

from .operations import operations as operations_cls
from .iterations import iterations as iterations_cls
from .fixed_zones import fixed_zones as fixed_zones_cls
from .indicator import indicator as indicator_cls
from .target import target as target_cls
from .adapt_mesh_1 import adapt_mesh as adapt_mesh_cls

class anisotropic_adaption(Group):
    fluent_name = ...
    child_names = ...
    operations: operations_cls = ...
    iterations: iterations_cls = ...
    fixed_zones: fixed_zones_cls = ...
    indicator: indicator_cls = ...
    target: target_cls = ...
    command_names = ...

    def adapt_mesh(self, ):
        """
        Adapt the mesh based on specified anisotropic adaption setup.
        """

    return_type = ...
