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

from .option_12 import option as option_cls

class reaction_mechs(Group):
    """
    Reaction-mechs property setting for this material.
    """

    fluent_name = "reaction-mechs"

    child_names = \
        ['option']

    _child_classes = dict(
        option=option_cls,
    )

