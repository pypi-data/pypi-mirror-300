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

from .option import option as option_cls
from .cone_type import cone_type as cone_type_cls
from .inject_as_film import inject_as_film as inject_as_film_cls

class injection_type(Group):
    """
    'injection_type' child.
    """

    fluent_name = "injection-type"

    child_names = \
        ['option', 'cone_type', 'inject_as_film']

    _child_classes = dict(
        option=option_cls,
        cone_type=cone_type_cls,
        inject_as_film=inject_as_film_cls,
    )

    return_type = "<object object at 0x7fe5b9e4c6e0>"
