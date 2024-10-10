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

from .gradient_scheme import gradient_scheme as gradient_scheme_cls
from .discretization_scheme import discretization_scheme as discretization_scheme_cls

class spatial_discretization(Group):
    """
    Spatial Discretizatio Schemes.
    """

    fluent_name = "spatial-discretization"

    child_names = \
        ['gradient_scheme', 'discretization_scheme']

    _child_classes = dict(
        gradient_scheme=gradient_scheme_cls,
        discretization_scheme=discretization_scheme_cls,
    )

