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

from .composition_dependent_specific_heat import composition_dependent_specific_heat as composition_dependent_specific_heat_cls
from .composition_dependent_density import composition_dependent_density as composition_dependent_density_cls

class multiple_surface_reactions(Group):
    """
    Multiple surface reactions setting.
    """

    fluent_name = "multiple-surface-reactions"

    child_names = \
        ['composition_dependent_specific_heat',
         'composition_dependent_density']

    _child_classes = dict(
        composition_dependent_specific_heat=composition_dependent_specific_heat_cls,
        composition_dependent_density=composition_dependent_density_cls,
    )

