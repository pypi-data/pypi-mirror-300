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

from .flux import flux as flux_cls
from .gradient import gradient as gradient_cls

class anisotropic_solid_heat_transfer(Group):
    """
    'anisotropic_solid_heat_transfer' child.
    """

    fluent_name = "anisotropic-solid-heat-transfer"

    child_names = \
        ['flux', 'gradient']

    _child_classes = dict(
        flux=flux_cls,
        gradient=gradient_cls,
    )

    return_type = "<object object at 0x7ff9d0b7b270>"
