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

from .blended_compressive_scheme import blended_compressive_scheme as blended_compressive_scheme_cls
from .pseudo_transient_stabilization import pseudo_transient_stabilization as pseudo_transient_stabilization_cls

class additional_stabilization_controls(Group):
    fluent_name = ...
    child_names = ...
    blended_compressive_scheme: blended_compressive_scheme_cls = ...
    pseudo_transient_stabilization: pseudo_transient_stabilization_cls = ...
    return_type = ...
