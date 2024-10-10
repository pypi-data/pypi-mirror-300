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

from .option_8 import option as option_cls
from .virtual_mass_factor import virtual_mass_factor as virtual_mass_factor_cls

class virtual_mass_force(Group):
    """
    'virtual_mass_force' child.
    """

    fluent_name = "virtual-mass-force"

    child_names = \
        ['option', 'virtual_mass_factor']

    _child_classes = dict(
        option=option_cls,
        virtual_mass_factor=virtual_mass_factor_cls,
    )

    return_type = "<object object at 0x7ff9d2a0de60>"
