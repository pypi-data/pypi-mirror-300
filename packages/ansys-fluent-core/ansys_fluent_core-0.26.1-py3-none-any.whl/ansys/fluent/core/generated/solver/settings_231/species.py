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

from .option_10 import option as option_cls

class species(Group):
    """
    'species' child.
    """

    fluent_name = "species"

    child_names = \
        ['option']

    _child_classes = dict(
        option=option_cls,
    )

    return_type = "<object object at 0x7ff9d14fd870>"
