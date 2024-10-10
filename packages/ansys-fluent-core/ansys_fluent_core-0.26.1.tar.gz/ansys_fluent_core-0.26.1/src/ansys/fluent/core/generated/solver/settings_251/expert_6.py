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

from .mass_flux_correction_method import mass_flux_correction_method as mass_flux_correction_method_cls
from .hybrid_mode_selection import hybrid_mode_selection as hybrid_mode_selection_cls

class expert(Group):
    """
    Enter overset expert solver options menu.
    """

    fluent_name = "expert"

    child_names = \
        ['mass_flux_correction_method', 'hybrid_mode_selection']

    _child_classes = dict(
        mass_flux_correction_method=mass_flux_correction_method_cls,
        hybrid_mode_selection=hybrid_mode_selection_cls,
    )

