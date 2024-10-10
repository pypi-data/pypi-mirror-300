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

from .use_vapor_species_heat_capacity import use_vapor_species_heat_capacity as use_vapor_species_heat_capacity_cls

class diffusion_controlled(Group):
    """
    Diffusion controlled settings.
    """

    fluent_name = "diffusion-controlled"

    child_names = \
        ['use_vapor_species_heat_capacity']

    _child_classes = dict(
        use_vapor_species_heat_capacity=use_vapor_species_heat_capacity_cls,
    )

