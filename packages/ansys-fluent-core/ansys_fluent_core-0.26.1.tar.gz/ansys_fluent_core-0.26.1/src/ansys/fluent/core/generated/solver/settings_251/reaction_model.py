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

class reaction_model(Group):
    """
    Set material property: reaction-model.
    """

    fluent_name = "reaction-model"

    child_names = \
        ['option']

    _child_classes = dict(
        option=option_cls,
    )

