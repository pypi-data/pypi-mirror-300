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

from .option_26 import option as option_cls
from .diffusion_controlled import diffusion_controlled as diffusion_controlled_cls
from .convection_diffusion_controlled import convection_diffusion_controlled as convection_diffusion_controlled_cls

class vaporization_model(Group):
    """
    Set material property: vaporization-model.
    """

    fluent_name = "vaporization-model"

    child_names = \
        ['option', 'diffusion_controlled', 'convection_diffusion_controlled']

    _child_classes = dict(
        option=option_cls,
        diffusion_controlled=diffusion_controlled_cls,
        convection_diffusion_controlled=convection_diffusion_controlled_cls,
    )

