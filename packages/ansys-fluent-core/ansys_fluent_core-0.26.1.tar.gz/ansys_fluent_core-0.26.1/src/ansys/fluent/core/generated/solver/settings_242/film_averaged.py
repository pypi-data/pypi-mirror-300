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

from .averaging_coefficient import averaging_coefficient as averaging_coefficient_cls
from .binary_diffusivity import binary_diffusivity as binary_diffusivity_cls

class film_averaged(Group):
    """
    Film averaged settings.
    """

    fluent_name = "film-averaged"

    child_names = \
        ['averaging_coefficient', 'binary_diffusivity']

    _child_classes = dict(
        averaging_coefficient=averaging_coefficient_cls,
        binary_diffusivity=binary_diffusivity_cls,
    )

