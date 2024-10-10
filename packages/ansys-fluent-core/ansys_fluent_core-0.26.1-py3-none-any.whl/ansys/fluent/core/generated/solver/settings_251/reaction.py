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

from .react import react as react_cls
from .reaction_mechs_1 import reaction_mechs as reaction_mechs_cls
from .surface_volume_ratio import surface_volume_ratio as surface_volume_ratio_cls
from .enable_12 import enable as enable_cls

class reaction(Group):
    """
    Allows to change reaction model variables or settings.
    """

    fluent_name = "reaction"

    child_names = \
        ['react', 'reaction_mechs', 'surface_volume_ratio', 'enable']

    _child_classes = dict(
        react=react_cls,
        reaction_mechs=reaction_mechs_cls,
        surface_volume_ratio=surface_volume_ratio_cls,
        enable=enable_cls,
    )

    _child_aliases = dict(
        electrolyte="enable",
    )

